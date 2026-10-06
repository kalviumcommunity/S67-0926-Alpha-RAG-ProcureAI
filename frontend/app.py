import streamlit as st

from styles import load_css


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="ProcureAI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# LOAD CSS
# ---------------------------------------------------------
load_css()


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-logo">
            <div class="logo-box">P</div>
            <div>
                <div class="logo-title">ProcureAI</div>
                <div class="logo-subtitle">Procurement Intelligence</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### Navigation")

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Documents",
            "Chat"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("### Upload Document")

    uploaded_file = st.file_uploader(
        "Upload procurement document",
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:

        if uploaded_file.name not in st.session_state.uploaded_files:
            st.session_state.uploaded_files.append(
                uploaded_file.name
            )

        st.success(
            f"{uploaded_file.name} uploaded"
        )

    st.markdown("---")

    st.markdown(
        """
        <div class="sidebar-footer">
            <div>ProcureAI</div>
            <small>AI-powered procurement assistant</small>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    # -----------------------------------------------------
    # PAGE HEADER
    # -----------------------------------------------------

    col1, col2 = st.columns([5, 1])

    with col1:

        st.markdown(
            """
<div class="page-title">
Procurement Intelligence
</div>

<div class="page-subtitle">
Search, understand and analyze your procurement documents.
</div>
""",
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
<div class="system-status">
<span class="status-dot"></span>
System Online
</div>
""",
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # WELCOME SECTION
    # -----------------------------------------------------

    st.markdown(
        """
<div class="welcome-card">

<div class="welcome-small">
AI PROCUREMENT ASSISTANT
</div>

<div class="welcome-title">
Your documents. Your answers.
</div>

<div class="welcome-text">
Upload procurement documents and ask natural-language
questions. ProcureAI will provide grounded answers
with supporting document references and page-level sources.
</div>

</div>
""",
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # DOCUMENT UPLOAD
    # -----------------------------------------------------

    st.markdown(
        """
<div class="section-title">
Documents
</div>
""",
        unsafe_allow_html=True
    )

    upload_col, info_col = st.columns([2, 1])

    with upload_col:

        dashboard_file = st.file_uploader(
            "Upload your procurement document",
            type=["pdf", "docx", "txt"],
            key="dashboard_uploader"
        )

        if dashboard_file is not None:

            if dashboard_file.name not in st.session_state.uploaded_files:

                st.session_state.uploaded_files.append(
                    dashboard_file.name
                )

            st.success(
                f"Successfully selected: {dashboard_file.name}"
            )


    with info_col:

        st.markdown(
            """
<div class="info-card">

<div class="info-title">
Supported Documents
</div>

<div class="info-text">
PDF, DOCX and TXT files
</div>

<div class="info-text">
Ask questions directly from your documents.
</div>

</div>
""",
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # STATISTICS
    # -----------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    stat1, stat2, stat3 = st.columns(3)

    with stat1:

        st.markdown(
            f"""
<div class="stat-card">

<div class="stat-number">
{len(st.session_state.uploaded_files)}
</div>

<div class="stat-label">
Documents
</div>

</div>
""",
            unsafe_allow_html=True
        )

    with stat2:

        st.markdown(
            f"""
<div class="stat-card">

<div class="stat-number">
{len(st.session_state.messages)}
</div>

<div class="stat-label">
Chat Messages
</div>

</div>
""",
            unsafe_allow_html=True
        )

    with stat3:

        st.markdown(
            """
<div class="stat-card">

<div class="stat-number">
AI
</div>

<div class="stat-label">
Assistant Status
</div>

</div>
""",
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # QUICK QUESTIONS
    # -----------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
<div class="section-title">
Quick Questions
</div>
""",
        unsafe_allow_html=True
    )

    q1, q2, q3 = st.columns(3)

    with q1:

        if st.button(
            "📄 Summarize this document",
            use_container_width=True
        ):

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": "Summarize this document."
                }
            )

            st.rerun()


    with q2:

        if st.button(
            "💰 Find pricing information",
            use_container_width=True
        ):

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": "Find the pricing information."
                }
            )

            st.rerun()


    with q3:

        if st.button(
            "📋 Find important requirements",
            use_container_width=True
        ):

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": "Find the important requirements."
                }
            )

            st.rerun()


# =========================================================
# DOCUMENTS PAGE
# =========================================================

elif page == "Documents":

    st.markdown(
        """
<div class="page-title">
Documents
</div>

<div class="page-subtitle">
Manage your procurement documents.
</div>
""",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if len(st.session_state.uploaded_files) == 0:

        st.info(
            "No documents uploaded yet."
        )

    else:

        for index, filename in enumerate(
            st.session_state.uploaded_files,
            start=1
        ):

            st.markdown(
                f"""
<div class="document-card">

<div class="document-icon">
📄
</div>

<div class="document-details">

<div class="document-name">
{filename}
</div>

<div class="document-status">
Ready for questions
</div>

</div>

</div>
""",
                unsafe_allow_html=True
            )


# =========================================================
# CHAT PAGE
# =========================================================

elif page == "Chat":

    st.markdown(
        """
<div class="page-title">
ProcureAI Assistant
</div>

<div class="page-subtitle">
Ask questions about your procurement documents.
</div>
""",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)


    # -----------------------------------------------------
    # PREVIOUS MESSAGES
    # -----------------------------------------------------

    for message in st.session_state.messages:

        role = message["role"]

        with st.chat_message(role):

            st.write(
                message["content"]
            )


    # -----------------------------------------------------
    # CHAT INPUT
    # -----------------------------------------------------

    question = st.chat_input(
        "Ask a question about your document..."
    )


    if question:

        # USER MESSAGE

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):

            st.write(question)


        # -------------------------------------------------
        # BACKEND PLACEHOLDER
        # -------------------------------------------------

        answer = (
            "Waiting for backend response..."
        )


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):

            st.write(answer)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
<div class="app-footer">
ProcureAI • AI-powered procurement document intelligence
</div>
""",
    unsafe_allow_html=True
)