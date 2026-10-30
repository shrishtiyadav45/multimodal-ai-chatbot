# Manual verification checklist

- [ ] Start backend and frontend using README commands; both launch without errors.
- [ ] `/api/health` returns `status: ok`.
- [ ] Send a normal text question; both sides of the conversation appear.
- [ ] Send an image with a question; preview and grounded answer appear.
- [ ] Send a short audio clip; playback preview and relevant answer appear.
- [ ] Try whitespace-only text; submission is blocked/rejected.
- [ ] Try a renamed text file as `.jpg`; backend rejects it before model call.
- [ ] Try unsupported/corrupted audio; backend returns a readable 4xx error.
- [ ] Try a file larger than `MAX_UPLOAD_MB`; backend returns 413.
- [ ] Stop backend and submit; frontend shows a connection error rather than hanging.
- [ ] Verify the API key exists only in `.env` and is absent from frontend code and API responses.
- [ ] Use Tab/Shift+Tab and Enter to navigate and submit.

Record Pass / Fail / Blocked and evidence for each check before submission.
