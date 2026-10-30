"""FastAPI backend for text, image, and audio chat."""
from io import BytesIO
from typing import Literal

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError

from backend.config import MAX_UPLOAD_BYTES, MAX_UPLOAD_MB, GEMINI_API_KEY
from backend.provider import generate_reply, ProviderNotConfigured

app = FastAPI(title="Study Buddy Chat API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

IMAGE_TYPES = {"image/jpeg": {".jpg", ".jpeg"}, "image/png": {".png"}, "image/webp": {".webp"}}
AUDIO_TYPES = {
    "audio/wav": {".wav"}, "audio/x-wav": {".wav"}, "audio/mpeg": {".mp3"},
    "audio/ogg": {".ogg"}, "application/ogg": {".ogg"}, "audio/webm": {".webm"},
    "audio/mp4": {".m4a", ".mp4"}, "audio/aac": {".aac"}, "audio/flac": {".flac"},
    "audio/x-flac": {".flac"},
}


def validate_image(data: bytes, content_type: str, filename: str) -> str:
    from pathlib import Path
    ext = Path(filename or "").suffix.lower()
    if content_type not in IMAGE_TYPES or ext not in IMAGE_TYPES[content_type]:
        raise HTTPException(415, "Unsupported image. Use a genuine JPG, PNG, or WebP file.")
    try:
        with Image.open(BytesIO(data)) as image:
            image.verify()
            actual = Image.MIME.get(image.format)
            if actual != content_type:
                raise HTTPException(415, "The image content does not match its file type.")
    except (UnidentifiedImageError, OSError, SyntaxError):
        raise HTTPException(415, "The image file is invalid or corrupted.") from None
    return content_type


def validate_audio(data: bytes, content_type: str, filename: str) -> str:
    from pathlib import Path
    ext = Path(filename or "").suffix.lower()
    allowed = AUDIO_TYPES.get(content_type)
    if not allowed or ext not in allowed:
        raise HTTPException(415, "Unsupported audio. Use WAV, MP3, OGG, WebM, M4A/MP4, AAC, or FLAC.")
    signatures = {
        ".wav": lambda b: len(b) > 12 and b[:4] == b"RIFF" and b[8:12] == b"WAVE",
        ".mp3": lambda b: b.startswith(b"ID3") or (len(b) > 1 and b[0] == 0xFF and (b[1] & 0xE0) == 0xE0),
        ".ogg": lambda b: b.startswith(b"OggS"),
        ".webm": lambda b: b.startswith(bytes.fromhex("1A45DFA3")),
        ".m4a": lambda b: len(b) > 12 and b[4:8] == b"ftyp",
        ".mp4": lambda b: len(b) > 12 and b[4:8] == b"ftyp",
        ".aac": lambda b: len(b) > 1 and b[0] == 0xFF and (b[1] & 0xF6) == 0xF0,
        ".flac": lambda b: b.startswith(b"fLaC"),
    }
    if not signatures[ext](data):
        raise HTTPException(415, "The audio file content is invalid or does not match its extension.")
    return content_type


@app.get("/api/health")
def health():
    return {"status": "ok", "provider_configured": bool(GEMINI_API_KEY), "max_upload_mb": MAX_UPLOAD_MB}


@app.post("/api/chat")
async def chat(
    modality: Literal["text", "image", "audio"] = Form(...),
    message: str = Form(default=""),
    file: UploadFile | None = File(default=None),
):
    prompt = (message or "").strip()
    if modality == "text" and not prompt:
        raise HTTPException(400, "Please type a message before sending.")
    if modality in {"image", "audio"} and file is None:
        raise HTTPException(400, f"Please attach an {modality} file.")

    file_bytes = None
    mime_type = None
    if file is not None:
        file_bytes = await file.read(MAX_UPLOAD_BYTES + 1)
        if not file_bytes:
            raise HTTPException(400, "The selected file is empty.")
        if len(file_bytes) > MAX_UPLOAD_BYTES:
            raise HTTPException(413, f"File is too large. Maximum upload size is {MAX_UPLOAD_MB} MB.")
        mime_type = file.content_type or ""
        if modality == "image":
            mime_type = validate_image(file_bytes, mime_type, file.filename or "")
        elif modality == "audio":
            mime_type = validate_audio(file_bytes, mime_type, file.filename or "")

    try:
        answer = generate_reply(prompt, modality, file_bytes, mime_type)
        return {"text": answer, "modality": modality}
    except ProviderNotConfigured as exc:
        raise HTTPException(503, str(exc)) from None
    except RuntimeError as exc:
        raise HTTPException(502, str(exc)) from None
    finally:
        if file is not None:
            await file.close()
