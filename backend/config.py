"""Server-side application configuration."""
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
MAX_UPLOAD_MB = max(1, int(os.getenv("MAX_UPLOAD_MB", "10")))
MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024
