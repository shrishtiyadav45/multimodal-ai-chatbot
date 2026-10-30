"""Gemini integration. Provider-specific code stays isolated from the API/UI."""
from backend.config import GEMINI_API_KEY, GEMINI_MODEL


class ProviderNotConfigured(RuntimeError):
    pass


def generate_reply(message: str, modality: str = "text", file_bytes: bytes | None = None,
                   mime_type: str | None = None) -> str:
    if not GEMINI_API_KEY:
        raise ProviderNotConfigured(
            "Gemini is not configured. Add GEMINI_API_KEY to your local .env file and restart the backend."
        )

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt = (message or "").strip()
        if modality == "image":
            prompt = prompt or "Describe the image. Mention only details that are visibly supported."
        elif modality == "audio":
            prompt = prompt or "Summarize the audio. If speech is present, provide a concise transcript-style summary."

        contents: list = [prompt]
        if file_bytes is not None:
            contents.append(types.Part.from_bytes(data=file_bytes, mime_type=mime_type or "application/octet-stream"))

        response = client.models.generate_content(model=GEMINI_MODEL, contents=contents)
        answer = (getattr(response, "text", None) or "").strip()
        if not answer:
            raise RuntimeError("The model returned an empty response. Please try again with a different input.")
        return answer
    except ProviderNotConfigured:
        raise
    except Exception as exc:
        # Do not return SDK internals, request payloads, or credentials to the client.
        message_text = str(exc).lower()
        if "429" in message_text or "quota" in message_text or "rate" in message_text:
            raise RuntimeError("The AI service is busy or the request quota was reached. Wait a moment and retry.") from None
        if "api key" in message_text or "unauthorized" in message_text or "401" in message_text:
            raise RuntimeError("The AI provider rejected the configured key. Check GEMINI_API_KEY in .env.") from None
        raise RuntimeError("The AI service could not complete this request. Check your connection and try again.") from None
