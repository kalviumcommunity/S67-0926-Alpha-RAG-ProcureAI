import html
import json
import os
import re

import requests
import streamlit as st

API = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/") + "/api"
SUPPLIER = "Uploaded documents"  # the backend requires a supplier; all uploads go under this one
REFUSAL_PREFIX = "I couldn't find enough information"
SUGGESTIONS = [
    "What are the payment terms?",
    "When does the contract expire?",
    "Are there late delivery penalties?",
    "Is auto-renewal notice required?",
]

st.set_page_config(page_title="ProcureAI", page_icon="📄", layout="centered")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Apply custom font specifically to text elements without touching icon fonts */
html, body, .stApp, p, span, div:not([data-testid="stIconMaterial"]):not(.material-symbols-rounded), button, input, textarea {
  font-family: 'Inter', sans-serif !important;
  font-variant-numeric: tabular-nums;
}

/* Ensure Streamlit expander icons retain their Material Icons font */
[data-testid="stExpander"] i,
[data-testid="stExpander"] [data-testid="stIconMaterial"],
[data-testid="stExpander"] .material-symbols-rounded {
  font-family: 'Material Symbols Rounded', 'Material Icons' !important;
  font-size: 20px !important;
  line-height: 1 !important;
}

/* Fix text layout inside expander header */
[data-testid="stExpander"] summary {
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
}

header[data-testid="stHeader"], #MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }
.stApp { background: #FAF9F9; }

/* one centered 720px column; 8px spacing scale; vertical gaps are set by margins below */
[data-testid="stMainBlockContainer"] { max-width: 720px !important; padding: 118px 24px 160px !important; }
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] { gap: 0; }
[data-testid="stBottom"] > div { background: #FAF9F9; }
[data-testid="stBottomBlockContainer"] { max-width: 720px !important; padding: 0 24px 24px !important; }
:focus-visible { outline: 2px solid #2447d8 !important; outline-offset: 2px; }
button, [data-testid="stFileUploaderDropzone"] { transition: border-color .15s ease, background .15s ease, box-shadow .15s ease; }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }

/* top bar, aligned to the column */
.topbar { position: fixed; top: 0; left: 0; right: 0; height: 54px; background: #fff; border-bottom: 1px solid #E4E4E7; z-index: 999; }
.topbar > div { max-width: 720px; margin: 0 auto; height: 100%; display: flex; align-items: center; justify-content: space-between; padding: 0 24px; }
.logo { display: inline-flex; align-items: center; justify-content: center; width: 28px; height: 28px; background: #111; color: #fff; border-radius: 8px; font-weight: 700; font-size: 14px; margin-right: 10px; }
.brand { font-weight: 600; font-size: 15px; } .tag { color: #52525B; font-size: 13px; border-left: 1px solid #E4E4E7; margin-left: 12px; padding-left: 12px; }
.badge { display: inline-flex; align-items: center; gap: 8px; background: #F4F4F5; border: 1px solid #E4E4E7; border-radius: 999px; padding: 6px 12px; font-size: 12px; font-weight: 500; color: #3F3F46; white-space: nowrap; }

/* hero */
.hero { text-align: center; }
.hero .badge { margin: 0; }
.hero h1 { font-size: 44px; line-height: 1.15; font-weight: 700; letter-spacing: -0.02em; text-wrap: balance; margin: 24px 0 0; padding: 0; }
.hero p { color: #52525B; font-size: 16px; line-height: 1.6; max-width: 520px; margin: 16px auto 0; text-wrap: balance; }

/* upload card (own box; no Streamlit border) */
.st-key-card { margin-top: 40px !important; background: #fff; border: 1px solid #E4E4E7; border-radius: 16px; padding: 24px !important; box-shadow: 0 1px 2px rgba(0,0,0,.04); gap: 16px !important; }
.st-key-card [data-testid="stMarkdown"], .st-key-card [data-testid="stElementContainer"] { margin: 0 !important; }
.st-key-card [data-testid="stFileUploader"] { margin: 0; }
.st-key-rows { gap: 0 !important; }
.cardhead { display: flex; justify-content: space-between; align-items: center; min-height: 28px; }
.cardhead b { font-size: 15px; font-weight: 600; }
.cardhead .badge { padding: 4px 10px; }
[data-testid="stFileUploaderDropzone"] { min-height: 180px; background: #FAFAFA; border: 2px dashed #D4D4D8; border-radius: 12px; padding: 32px; flex-direction: column; align-items: center; justify-content: center; gap: 12px; text-align: center; }
[data-testid="stFileUploaderDropzone"]:hover { border-color: #71717A; background: #F4F4F5; }
[data-testid="stFileUploaderDropzoneInstructions"] { display: flex; flex-direction: column; align-items: center; gap: 12px; margin: 0; }
[data-testid="stFileUploaderDropzoneInstructions"] svg { box-sizing: content-box; width: 24px; height: 24px; padding: 12px; border-radius: 50%; background: #EAF0FF; color: #2447d8; }
[data-testid="stFileUploaderDropzoneInstructions"] > div { display: flex; flex-direction: column; align-items: center; gap: 4px; }
[data-testid="stFileUploaderDropzoneInstructions"] > div > span:first-child::before { content: "Drag and drop supplier contracts here"; font-size: 15px; font-weight: 600; color: #111; line-height: 1.4; }
[data-testid="stFileUploaderDropzoneInstructions"] > div > span:last-child::before { content: "or click to browse · PDF only · up to 20MB per file"; font-size: 13px; color: #52525B; line-height: 1.5; }
[data-testid="stFileUploaderDropzone"] button { height: 40px; padding: 0 16px; margin-top: -8px; border-radius: 8px; background: #fff; color: #111; border: 1px solid #D4D4D8; font-size: 14px; font-weight: 500; }
[data-testid="stFileUploaderDropzone"] button:hover { border-color: #111; background: #fff; color: #111; }
.status { display: flex; align-items: center; gap: 8px; font-size: 13px; line-height: 1.5; color: #52525B; }
.dot { width: 8px; height: 8px; border-radius: 50%; background: #F59E0B; } .dot.ok { background: #16A34A; }
[class*="st-key-row"] { border-bottom: 1px solid #E4E4E7; min-height: 48px; }
[class*="st-key-row"] [data-testid="stHorizontalBlock"] { align-items: center; gap: 8px; }
.fname { display: flex; align-items: center; gap: 8px; min-width: 0; font-size: 14px; }
.fname span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.meta { font-size: 13px; color: #52525B; white-space: nowrap; }
[class*="st-key-del"] button { width: 40px; height: 40px; padding: 0; border-radius: 8px; border: 0; background: transparent; color: #52525B; }
[class*="st-key-del"] button:hover { background: #F4F4F5; color: #111; }

/* buttons, suggestions */
.stButton { width: 100%; }
.stButton > button, [data-testid="stPopover"] > button { border-radius: 8px; border: 1px solid #D4D4D8; background: #fff; color: #111; font-size: 14px; font-weight: 500; min-height: 40px; padding: 0 16px; }
.stButton > button:hover, [data-testid="stPopover"] > button:hover { border-color: #111; color: #111; }
.st-key-suggest { margin-top: 32px !important; gap: 12px !important; }
.st-key-suggest [data-testid="stMarkdown"] { margin: 0 0 4px 0 !important; }
.label { font-size: 13px; line-height: 1.5; color: #52525B; margin: 0; padding-bottom: 2px; }
.st-key-chips { gap: 12px !important; }
.st-key-chips [data-testid="stHorizontalBlock"] { gap: 12px !important; }
.st-key-chips [data-testid="stColumn"] > [data-testid="stVerticalBlock"] { gap: 12px !important; }
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] > [data-testid="stElementContainer"] { margin: 0 !important; }
.st-key-chips button { height: 44px; width: 100%; justify-content: flex-start; padding: 0 16px; font-size: 14px; font-weight: 400; }
.st-key-chips button p { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; margin: 0; line-height: 1.4; }
.st-key-chips button:hover:not(:disabled) { box-shadow: 0 2px 8px rgba(0,0,0,.08); }
.st-key-chips button:disabled { opacity: .6; cursor: not-allowed; }
.st-key-inputwrap { margin-top: 40px !important; }

/* chat input styling */
[data-testid="stChatInput"] { min-height: 56px; border-radius: 16px; border: 1px solid #E4E4E7; background: #fff; box-shadow: 0 4px 16px rgba(0,0,0,.06); align-items: center; }
[data-testid="stAlert"] { margin-top: 16px; }

/* conversation */
.ub { margin: 0 0 16px auto; width: fit-content; max-width: 85%; background: #fff; border: 1px solid #E4E4E7; border-radius: 14px; padding: 10px 16px; font-size: 14px; }
[data-testid="stVerticalBlockBorderWrapper"] { background: #fff; border: 1px solid #E4E4E7; border-radius: 14px; box-shadow: 0 1px 2px rgba(0,0,0,.04); margin-bottom: 16px; }
.ahead { display: flex; align-items: center; gap: 8px; font-weight: 600; font-size: 13px; margin-bottom: 6px; }
.avatar { width: 22px; height: 22px; border-radius: 50%; background: #111; color: #fff; display: inline-flex; align-items: center; justify-content: center; font-size: 11px; }
.srclabel { font-size: 12px; color: #52525B; margin: 10px 0 6px; }
.pill { display: inline-block; background: #F4F4F5; border: 1px solid #E4E4E7; border-radius: 8px; margin: 0 8px 6px 0; padding: 5px 10px; font-size: 12px; color: #333; }

@media (max-width: 640px) {
  [data-testid="stMainBlockContainer"], [data-testid="stBottomBlockContainer"] { padding-left: 16px !important; padding-right: 16px !important; }
  .hero h1 { font-size: 28px; }
  .st-key-card { padding: 16px; }
  [data-testid="stFileUploaderDropzone"] { min-height: 160px; padding: 24px 16px; }
  .tag { display: none; }
}
</style>
""",
    unsafe_allow_html=True,
)


class ApiError(Exception):
    pass


def _detail(r):
    try:
        d = r.json().get("detail")
    except ValueError:
        d = None
    if isinstance(d, list):
        d = "; ".join(str(x.get("msg", "")) for x in d)
    return d or f"Request failed ({r.status_code})"


def call(method, path, timeout=30, **kw):
    try:
        r = requests.request(method, f"{API}{path}", timeout=timeout, **kw)
    except requests.RequestException:
        raise ApiError(f"Cannot reach the backend at {API}. Is it running?")
    if not r.ok:
        raise ApiError(_detail(r))
    return r.json()


def ingest(file):
    """Upload one PDF (the backend processes it during the upload). Returns an error string or None."""
    try:
        supplier = next((s["id"] for s in call("GET", "/suppliers") if s["name"] == SUPPLIER), None)
        if supplier is None:
            supplier = call("POST", "/suppliers", json={"name": SUPPLIER})["id"]
        call(
            "POST", "/documents/upload", timeout=900,
            files={"file": (file.name, file.getvalue(), "application/pdf")},
            data={"supplier_id": supplier, "document_type": "other"},
        )
    except ApiError as e:
        return f"Could not add {file.name}: {e}"
    return None


def stream_chat(question):
    try:
        with requests.post(f"{API}/chat/stream", json={"question": question}, stream=True, timeout=120) as r:
            if not r.ok:
                raise ApiError(_detail(r))
            r.encoding = "utf-8"
            event = None
            for line in r.iter_lines(decode_unicode=True):
                if line.startswith("event:"):
                    event = line[6:].strip()
                elif line.startswith("data:") and event:
                    yield event, json.loads(line[5:].strip())
    except requests.RequestException:
        raise ApiError("Lost connection to the backend while answering.")


_MARKER = re.compile(r"\s*[【\[][^】\]]*(?:Source|Document ID|Chunk)[^】\]]*[】\]]", re.IGNORECASE)


def clean(text):
    """Remove leftover citation markers the model may still emit."""
    return _MARKER.sub("", text).strip()


ss = st.session_state
ss.setdefault("messages", [])
ss.setdefault("up_n", 0)
ss.setdefault("flash", [])

BRAND = '<div class="ahead"><span class="avatar">P</span>ProcureAI Grounded Synthesis</div>'
SHIELD = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#2447d8" stroke-width="2" '
          'stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/></svg>')
FILE = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#52525B" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V8z"/><path d="M14 3v5h5"/></svg>')


def human_size(n):
    if not n:
        return ""
    return f"{n / 1024:.0f} KB" if n < 1024 * 1024 else f"{n / 1024 / 1024:.1f} MB"


def render(m):
    if m["role"] == "user":
        st.markdown(f'<div class="ub">{html.escape(m["content"])}</div>', unsafe_allow_html=True)
        return
    with st.container(border=True):
        st.markdown(BRAND, unsafe_allow_html=True)
        st.markdown(m["content"])
        if m.get("error"):
            st.error(m["error"])
        sources = m.get("sources") or []
        if sources:
            names = list(dict.fromkeys(f"{s['document_name']} · Page {s['page']}" for s in sources))
            pills = "".join(f'<span class="pill">📄 {html.escape(n)}</span>' for n in names)
            st.markdown(f'<div class="srclabel">Sources</div>{pills}', unsafe_allow_html=True)
            with st.expander("View excerpts"):
                for s in sources:
                    st.markdown(f"**{s['document_name']}** · page {s['page']}")
                    st.caption(s["excerpt"])


def answer(question):
    with st.container(border=True):
        st.markdown(BRAND, unsafe_allow_html=True)
        box = st.empty()
        text, sources, error = "", [], None
        try:
            for ev, data in stream_chat(question):
                if ev == "chunk":
                    text += data["content"]
                    box.markdown(clean(text) + "▌")
                elif ev == "sources":
                    sources = data["sources"]
                elif ev == "error":
                    error = data.get("detail", "Unknown error")
        except ApiError as e:
            error = str(e)
        if error and error.startswith(REFUSAL_PREFIX):
            text, error, sources = error, None, []  # backend rejected the streamed answer
        box.markdown(clean(text))
    return {"role": "assistant", "content": clean(text), "sources": sources, "error": error}


def add_files(files, pending_text=""):
    with st.spinner("Processing documents (the first one takes a while)…"):
        errors = [e for e in (ingest(f) for f in files) if e]
    ss.up_n += 1
    ss.flash = errors
    if pending_text:
        ss.pending_q = pending_text
    st.rerun()


def set_question(q):
    ss.pending_q = q


# ------------------------------------------------------------------ data
try:
    call("GET", "/health")
    docs = call("GET", "/documents")
except ApiError as e:
    st.error(str(e))
    st.stop()
ready = [d for d in docs if d["status"] == "processed"]
n = len(ready)
chatting = bool(ss.messages)
plural = "s" if n != 1 else ""

# ------------------------------------------------------------------ top bar + hero
st.markdown(
    '<div class="topbar"><div><div style="display:flex;align-items:center">'
    '<span class="logo">P</span><span class="brand">ProcureAI</span>'
    '<span class="tag">Supplier Contract Intelligence</span></div>'
    f'<span class="badge">📄 {n} document{plural}</span></div></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero">'
    + (f'<span class="badge">{SHIELD}ProcureAI Contract Engine · Grounded answers</span>' if not chatting else "")
    + "<h1>Ask questions about your supplier contracts.</h1>"
    "<p>Find negotiated payment terms, pricing schedules, late fulfillment penalties, "
    "renewal windows, and compliance obligations.</p></div>",
    unsafe_allow_html=True,
)
for err in ss.flash:
    st.error(err)
ss.flash = []

# ------------------------------------------------------------------ upload card
with st.container(key="card"):
    st.markdown(
        f'<div class="cardhead"><b>Active Supplier Repositories</b><span class="badge">{len(docs)} uploaded</span></div>',
        unsafe_allow_html=True,
    )
    if not chatting:
        up = st.file_uploader(
            "Upload supplier contracts", type=["pdf"], accept_multiple_files=True,
            key=f"up{ss.up_n}", label_visibility="collapsed",
        )
        if up:
            add_files(up)
    else:
        with st.popover("＋ Add documents"):
            more = st.file_uploader("Add PDFs", type=["pdf"], accept_multiple_files=True, key=f"more{ss.up_n}", label_visibility="collapsed")
            if more:
                add_files(more)
    rows = st.container(key="rows")
    for d in docs:
        with rows.container(key=f"row{d['id']}"):
            c1, c2, c3 = st.columns([6, 2, 1], vertical_alignment="center")
            c1.markdown(f'<div class="fname">{FILE}<span title="{html.escape(d["filename"])}">{html.escape(d["filename"])}</span></div>', unsafe_allow_html=True)
            state = "Indexed" if d["status"] == "processed" else "Failed"
            c2.markdown(f'<div class="meta">{human_size(d.get("file_size"))} · {state}</div>', unsafe_allow_html=True)
            if c3.button("✕", key=f"del{d['id']}", help=f"Remove {d['filename']}"):
                try:
                    call("DELETE", f"/documents/{d['id']}")
                except ApiError as e:
                    st.error(str(e))
                else:
                    st.rerun()
    status = (f'<span class="dot ok"></span>Ready · {n} document{plural} indexed' if n
              else '<span class="dot"></span>Waiting for documents')
    st.markdown(f'<div class="status">{status}</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------ conversation
question = ss.pop("pending_q", None)
if question and not ready:
    st.warning("Upload a contract first, then ask your question.")
    question = ""
if question:
    ss.messages.append({"role": "user", "content": question})
if chatting or question:
    st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)
for m in ss.messages:
    render(m)
if question:
    ss.messages.append(answer(question))
    st.rerun()  # re-render from state so the chips and docked input update

# ------------------------------------------------------------------ suggestions
label = "Suggested:" if chatting else ("Try asking:" if ready else "Once documents are uploaded, try asking:")
with st.container(key="suggest"):
    st.markdown(f'<div class="label">{label}</div>', unsafe_allow_html=True)
    with st.container(key="chips"):
        cols = st.columns(2)
        for i, s in enumerate(SUGGESTIONS):
            cols[i % 2].button(
                s, key=f"sug{i}", disabled=not ready, on_click=set_question, args=(s,),
                help=None if ready else "Upload a contract to enable",
            )

# ------------------------------------------------------------------ chat input (inline on the landing page, docked once chatting)
placeholder = "Ask anything about your supplier contracts…" if ready else "Upload a contract to start asking questions…"
if chatting:
    sub = st.chat_input(placeholder, accept_file="multiple", file_type=["pdf"])
else:
    with st.container(key="inputwrap"):
        sub = st.chat_input(placeholder, accept_file="multiple", file_type=["pdf"])
if sub:
    typed = (sub.text or "").strip()
    if sub.files:
        add_files(sub.files, typed)
    elif typed:
        ss.pending_q = typed
        st.rerun()