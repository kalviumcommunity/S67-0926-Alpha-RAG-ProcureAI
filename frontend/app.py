import streamlit as st
from styles import load_css

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="ProcureAI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_css()


# ==============================
# SESSION STATE
# ==============================

if "documents" not in st.session_state:
    st.session_state.documents = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if "questions" not in st.session_state:
    st.session_state.questions = 0


# ==============================
# SIDEBAR
# ==============================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-logo">◈</div>
            <div class="sidebar-brand-name">ProcureAI</div>
            <div class="sidebar-brand-subtitle">
                Intelligent Procurement Assistant
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("＋ New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        '<div class="sidebar-section">Workspace</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-item sidebar-item-active">
            ◈ Document Q&A
        </div>

        <div class="sidebar-item">
            ◫ Documents
        </div>

        <div class="sidebar-item">
            ◉ Conversation History
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-section">Session</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="sidebar-item">
            Documents: {len(st.session_state.documents)}
        </div>

        <div class="sidebar-item">
            Questions: {st.session_state.questions}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-footer">
            <div class="sidebar-footer-title">
                ProcureAI Workspace
            </div>

            <div class="sidebar-footer-text">
                Upload procurement documents and ask questions
                using grounded AI answers.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==============================
# TOP BAR
# ==============================

st.markdown(
    """
    <div class="topbar">

        <div class="brand">

            <div class="brand-logo">
                ◈
            </div>

            <div>
                <div class="brand-name">
                    ProcureAI
                </div>

                <div class="brand-subtitle">
                    Procurement Intelligence Platform
                </div>
            </div>

        </div>

        <div class="status-pill">
            <span class="status-dot"></span>
            System Online
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ==============================
# HERO
# ==============================

st.markdown(
    """
    <div class="hero">

        <div class="hero-label">
            AI Procurement Assistant
        </div>

        <div class="hero-title">
            Ask your procurement documents anything.
        </div>

        <div class="hero-text">
            Upload procurement documents and get fast,
            grounded answers with supporting document
            references and page-level sources.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ==============================
# STAT CARDS
# ==============================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-icon">◫</div>
            <div class="stat-label">Documents</div>
            <div class="stat-value">
                {len(st.session_state.documents)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-icon">?</div>
            <div class="stat-label">Questions</div>
            <div class="stat-value">
                {st.session_state.questions}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-icon">⌁</div>
            <div class="stat-label">AI Status</div>
            <div class="stat-value">
                Ready
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-icon">✓</div>
            <div class="stat-label">Sources</div>
            <div class="stat-value">
                Grounded
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==============================
# DOCUMENT UPLOAD
# ==============================

st.markdown(
    '<div class="section-title">Document Workspace</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section-description">
        Upload procurement documents to begin asking questions.
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_files = st.file_uploader(
    "Upload procurement documents",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
    help="Supported formats: PDF, DOCX and TXT"
)

if uploaded_files:

    for file in uploaded_files:

        if file.name not in st.session_state.documents:
            st.session_state.documents.append(file.name)

    st.success(
        f"{len(uploaded_files)} document(s) uploaded successfully."
    )


# ==============================
# DOCUMENT LIST
# ==============================

if st.session_state.documents:

    st.markdown(
        '<div class="section-title">Uploaded Documents</div>',
        unsafe_allow_html=True
    )

    document_columns = st.columns(
        min(len(st.session_state.documents), 3)
    )

    for index, document in enumerate(
        st.session_state.documents
    ):

        with document_columns[
            index % len(document_columns)
        ]:

            st.markdown(
                f"""
                <div class="document-card">

                    <div class="document-icon">
                        ◫
                    </div>

                    <div class="document-name">
                        {document}
                    </div>

                    <div class="document-meta">
                        Procurement document
                    </div>

                    <div class="document-status">
                        Ready
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# ==============================
# MAIN WORKSPACE
# ==============================

st.markdown(
    '<div class="section-title">Ask ProcureAI</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section-description">
        Ask questions about your uploaded procurement documents.
    </div>
    """,
    unsafe_allow_html=True
)


# ==============================
# CHAT HISTORY
# ==============================

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="chat-user">
                <strong>You</strong><br>
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="chat-ai">

                <div class="ai-label">
                    ProcureAI
                </div>

                {message["content"]}

            </div>
            """,
            unsafe_allow_html=True
        )


# ==============================
# CHAT INPUT
# ==============================

question = st.chat_input(
    "Ask a question about your procurement documents..."
)

if question:

    st.session_state.questions += 1

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # Temporary response.
    # This will later be replaced by Person 1's backend API.

    answer = (
        "I received your question. "
        "The backend RAG API will be connected here. "
        "Once connected, ProcureAI will analyze the uploaded "
        "documents and return a grounded answer with "
        "supporting sources."
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.rerun()


# ==============================
# SOURCES
# ==============================

st.markdown(
    '<div class="section-title">Sources</div>',
    unsafe_allow_html=True
)

if st.session_state.messages:

    st.markdown(
        """
        <div class="source-card">

            <div class="source-title">
                Document sources will appear here
            </div>

            <div class="source-meta">
                Backend integration required for document,
                page number and reference information.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.info(
        "Sources will appear here after you ask a question."
    )


# ==============================
# CAPABILITIES
# ==============================

st.markdown(
    '<div class="section-title">ProcureAI Capabilities</div>',
    unsafe_allow_html=True
)

cap1, cap2, cap3 = st.columns(3)

with cap1:

    st.markdown(
        """
        <div class="capability-card">

            <div class="capability-icon">
                📄
            </div>

            <div class="capability-title">
                Document Understanding
            </div>

            <div class="capability-text">
                Analyze procurement documents and
                extract relevant information.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with cap2:

    st.markdown(
        """
        <div class="capability-card">

            <div class="capability-icon">
                💬
            </div>

            <div class="capability-title">
                Intelligent Q&A
            </div>

            <div class="capability-text">
                Ask natural-language questions and
                receive contextual answers.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with cap3:

    st.markdown(
        """
        <div class="capability-card">

            <div class="capability-icon">
                🔎
            </div>

            <div class="capability-title">
                Source References
            </div>

            <div class="capability-text">
                View supporting documents, page numbers
                and references for generated answers.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==============================
# FOOTER
# ==============================

st.markdown(
    """
    <div class="footer">
        ProcureAI · Intelligent Procurement Document Assistant
    </div>
    """,
    unsafe_allow_html=True
)