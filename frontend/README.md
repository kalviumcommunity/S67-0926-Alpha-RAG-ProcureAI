# ProcureAI - Streamlit frontend

One-page chat UI for the FastAPI backend (see `backend/API.md`).

## Run

```bash
# terminal 1 - backend
cd backend && source .venv/bin/activate
python3 -m uvicorn app.main:app --reload

# terminal 2 - frontend
cd frontend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Opens at http://localhost:8501. Backend URL defaults to `http://127.0.0.1:8000`;
override with `API_BASE_URL=https://your-backend streamlit run app.py`.

## Use
- Click the attach button in the message box to add one or more PDFs; each is uploaded and processed during the upload request.
- Type a question and press Enter. Answers stream in with sources (document, page, excerpt).
- "New chat" clears the on-screen conversation. Chat history lasts for the browser session.

## Notes
- Every upload is stored under a supplier called "Uploaded documents" with type "other" (the backend requires both).
- Only PDFs can be processed by the backend right now.
- Questions search all processed documents. Each question is answered on its own (no follow-up memory yet).
- The backend runs its grounding check after streaming, so the UI replaces streamed text when an answer is rejected.
