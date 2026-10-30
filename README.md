# Study Buddy Chat — Python-only Multimodal Chatbot

A complete beginner-friendly project for the Module 3 multimodal chatbot lab. **Both frontend and backend are Python.** The UI is built with Streamlit; the API is built with FastAPI. There are no custom JavaScript, HTML, CSS, or Node.js files.

## Features
- Text conversation with a multimodal Gemini model
- Image upload and question answering (JPG, JPEG, PNG, WebP)
- Audio upload and summarization (WAV, MP3, OGG, WebM, M4A/MP4, AAC, FLAC; actual provider support can vary)
- File preview, loading state, readable errors, retry, and clear conversation
- Server-side upload validation (size, MIME type, extension, image decoding/audio signature)
- API key kept on backend only; no database or persistent media storage
- Automated backend tests with mocked provider responses

## Project structure
```text
study-buddy-python/
├── backend/
│   ├── config.py          # server-side environment configuration
│   ├── main.py            # FastAPI routes and upload validation
│   └── provider.py        # Gemini SDK integration
├── frontend/
│   └── app.py             # Streamlit UI (Python only)
├── tests/test_api.py
├── docs/MANUAL_TESTS.md
├── .env.example
├── SPEC.md
└── requirements.txt
```

## Requirements
- Python 3.10 or newer
- Internet connection for Gemini responses
- A Gemini API key from Google AI Studio

## Windows setup (PowerShell)
Open a terminal in this folder:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```
Edit `.env` and add your real `GEMINI_API_KEY`. Never paste the key into source code, Streamlit UI, screenshots, or version control.

## macOS / Linux setup
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```
Edit `.env` and add your key.

## Run (two terminals)
Terminal 1 — backend:
```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```
Terminal 2 — Python frontend:
```bash
streamlit run frontend/app.py
```
Open the Streamlit URL shown in the terminal (normally `http://localhost:8501`). FastAPI docs are at `http://127.0.0.1:8000/docs` and health is at `http://127.0.0.1:8000/api/health`.

## Configuration
| Variable | Default | Purpose |
|---|---|---|
| `GEMINI_API_KEY` | empty | Secret key; required for real model responses |
| `GEMINI_MODEL` | `gemini-2.5-flash` | Gemini model ID |
| `MAX_UPLOAD_MB` | `10` | Maximum media upload size |
| `BACKEND_URL` | `http://127.0.0.1:8000` | FastAPI URL used by Streamlit |

## Run tests
```bash
pytest -q
```
Tests mock Gemini calls and do not require an API key. A successful test run does not replace the manual live image/audio verification; complete `docs/MANUAL_TESTS.md` too.

## Privacy and limitations
Media is read in memory, validated by the backend, and sent to Google Gemini for inference. It is not saved to a project uploads folder or database. Google's provider data handling and model availability apply. Do not upload private/sensitive media. This is a local educational demo, not production-ready. Before public deployment, add authentication, rate limiting, HTTPS, monitoring, strict deployment CORS settings, and privacy controls.
