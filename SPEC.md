# Study Buddy Chat — Product Specification

## Purpose
A small educational chatbot that accepts text, one image, or one audio clip and returns a concise text answer.

## Architecture (Python only)
- Frontend: Streamlit (`frontend/app.py`) — all UI is authored in Python.
- Backend: FastAPI (`backend/`) — validation and model-provider calls.
- Provider: Google Gemini through the official `google-genai` Python SDK.
- No custom JavaScript, HTML, CSS, Node.js, database, or persistent media storage.

## Acceptance criteria
| ID | Requirement | Acceptance check |
|---|---|---|
| F1 | Text chat | Send a non-empty question and see user and assistant messages. |
| F2 | Image understanding | Attach JPG/PNG/WebP with an optional question; response is grounded in the image. |
| F3 | Audio understanding | Attach supported audio and receive a summary/transcript-style answer. |
| F4 | Feedback/retry | Loading, success and readable failure states; failed input can be retried. |
| N1 | Secret handling | Gemini key is read only by backend from `.env`; never sent to Streamlit/browser. |
| N2 | Upload validation | Backend checks size, MIME, extension and media signatures before provider call. |
| N3 | Accessibility | Streamlit native labelled controls, keyboard navigation, and visible status feedback. |

## Constraints
- Stateless server; conversation history exists only in Streamlit session state.
- Maximum upload size defaults to 10 MB.
- No logging or long-term storage of uploaded media.
- Provider output is rendered as Markdown text, never as executable HTML.
