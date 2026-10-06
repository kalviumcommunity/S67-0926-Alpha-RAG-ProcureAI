import streamlit as st


def load_css():

    st.markdown(
        """
<style>

/* =========================================================
   GLOBAL
========================================================= */

.stApp {
    background: #f7f8fc;
}

.main .block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}


/* =========================================================
   SIDEBAR
========================================================= */

section[data-testid="stSidebar"] {
    background: #0f172a;
    border-right: 1px solid #1e293b;
}

section[data-testid="stSidebar"] > div {
    background: #0f172a;
}

section[data-testid="stSidebar"] * {
    color: #e5e7eb;
}


/* Sidebar logo */

.sidebar-logo-wrapper {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 4px 28px 4px;
}

.sidebar-logo {
    width: 42px;
    height: 42px;
    border-radius: 13px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: linear-gradient(
        135deg,
        #6366f1,
        #8b5cf6
    );

    color: white;
    font-size: 19px;
    font-weight: 800;

    box-shadow:
        0 8px 25px rgba(99, 102, 241, 0.35);
}

.sidebar-brand {
    display: flex;
    flex-direction: column;
}

.sidebar-brand-name {
    color: white;
    font-size: 18px;
    font-weight: 800;
}

.sidebar-brand-subtitle {
    color: #94a3b8;
    font-size: 10px;
    margin-top: 2px;
}


/* Sidebar section */

.sidebar-section {
    color: #64748b;
    font-size: 10px;
    font-weight: 800;

    text-transform: uppercase;
    letter-spacing: 1px;

    margin-top: 20px;
    margin-bottom: 9px;
}


/* Sidebar navigation */

.sidebar-nav {
    padding: 10px 12px;
    border-radius: 10px;

    color: #cbd5e1;
    font-size: 13px;

    margin-bottom: 4px;
}

.sidebar-nav-active {
    background: #1e293b;
    color: white;

    border: 1px solid #334155;
}


/* Sidebar workspace card */

.sidebar-workspace {
    margin-top: 25px;

    padding: 15px;

    border-radius: 14px;

    background: #172033;
    border: 1px solid #273449;
}

.sidebar-workspace-title {
    color: white;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 6px;
}

.sidebar-workspace-text {
    color: #94a3b8;
    font-size: 10px;
    line-height: 1.6;
}


/* =========================================================
   TOP HEADER
========================================================= */

.top-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    margin-bottom: 30px;
}

.page-title {
    font-size: 27px;
    font-weight: 800;
    color: #111827;

    letter-spacing: -0.5px;
}

.page-subtitle {
    color: #64748b;
    font-size: 13px;
    margin-top: 5px;
}


/* Status */

.system-status {
    display: flex;
    align-items: center;
    gap: 8px;

    padding: 8px 13px;

    border-radius: 20px;

    background: #ecfdf5;
    border: 1px solid #bbf7d0;

    color: #047857;

    font-size: 11px;
    font-weight: 700;
}

.status-dot {
    width: 7px;
    height: 7px;

    border-radius: 50%;

    background: #10b981;
}


/* =========================================================
   WELCOME CARD
========================================================= */

.welcome-card {
    position: relative;

    overflow: hidden;

    background:
        linear-gradient(
            135deg,
            #111827 0%,
            #1e1b4b 55%,
            #312e81 100%
        );

    border-radius: 22px;

    padding: 35px;

    margin-bottom: 25px;

    box-shadow:
        0 15px 40px rgba(15, 23, 42, 0.14);
}

.welcome-card::after {
    content: "";

    position: absolute;

    width: 260px;
    height: 260px;

    border-radius: 50%;

    background: rgba(139, 92, 246, 0.18);

    right: -70px;
    top: -120px;
}

.welcome-small {
    position: relative;
    z-index: 2;

    color: #c4b5fd;

    font-size: 11px;
    font-weight: 800;

    text-transform: uppercase;

    letter-spacing: 1px;

    margin-bottom: 10px;
}

.welcome-title {
    position: relative;
    z-index: 2;

    color: white;

    font-size: 30px;
    font-weight: 800;

    letter-spacing: -0.7px;

    margin-bottom: 10px;
}

.welcome-text {
    position: relative;
    z-index: 2;

    color: #cbd5e1;

    font-size: 13px;

    line-height: 1.7;

    max-width: 650px;
}


/* =========================================================
   QUICK STATS
========================================================= */

.stat-card {
    background: white;

    border: 1px solid #e5e7eb;

    border-radius: 16px;

    padding: 17px;

    min-height: 100px;

    box-shadow:
        0 4px 15px rgba(15, 23, 42, 0.035);
}

.stat-icon {
    width: 34px;
    height: 34px;

    border-radius: 9px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #eef2ff;

    color: #4f46e5;

    font-size: 16px;

    margin-bottom: 10px;
}

.stat-label {
    color: #64748b;

    font-size: 10px;

    text-transform: uppercase;

    letter-spacing: 0.5px;

    font-weight: 700;
}

.stat-value {
    color: #111827;

    font-size: 20px;

    font-weight: 800;

    margin-top: 3px;
}


/* =========================================================
   SECTION
========================================================= */

.section-heading {
    display: flex;
    align-items: center;
    justify-content: space-between;

    margin-top: 30px;
    margin-bottom: 12px;
}

.section-title {
    color: #111827;

    font-size: 18px;

    font-weight: 800;
}

.section-description {
    color: #64748b;

    font-size: 12px;

    margin-top: 3px;
}


/* =========================================================
   UPLOAD AREA
========================================================= */

.upload-card {
    background: white;

    border: 1px solid #e5e7eb;

    border-radius: 18px;

    padding: 20px;

    box-shadow:
        0 4px 15px rgba(15, 23, 42, 0.035);
}

[data-testid="stFileUploader"] {
    background: #fafbff;

    border: 2px dashed #c7d2fe;

    border-radius: 14px;

    padding: 8px;
}

[data-testid="stFileUploader"]:hover {
    border-color: #818cf8;

    background: #f8f8ff;
}


/* =========================================================
   DOCUMENT CARDS
========================================================= */

.document-card {
    background: white;

    border: 1px solid #e5e7eb;

    border-radius: 15px;

    padding: 17px;

    min-height: 145px;

    box-shadow:
        0 4px 15px rgba(15, 23, 42, 0.035);
}

.document-icon {
    width: 38px;
    height: 38px;

    border-radius: 10px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #eef2ff;

    color: #4f46e5;

    font-size: 17px;

    margin-bottom: 12px;
}

.document-name {
    color: #111827;

    font-size: 13px;

    font-weight: 750;

    word-break: break-word;

    line-height: 1.4;
}

.document-type {
    color: #94a3b8;

    font-size: 10px;

    margin-top: 4px;
}

.document-ready {
    display: inline-block;

    margin-top: 12px;

    padding: 5px 9px;

    border-radius: 20px;

    background: #ecfdf5;

    color: #047857;

    font-size: 9px;

    font-weight: 800;
}


/* =========================================================
   CHAT
========================================================= */

.chat-header {
    display: flex;

    align-items: center;

    justify-content: space-between;

    margin-top: 30px;

    margin-bottom: 15px;
}

.chat-title {
    color: #111827;

    font-size: 19px;

    font-weight: 800;
}

.chat-subtitle {
    color: #64748b;

    font-size: 12px;

    margin-top: 3px;
}

.chat-badge {
    padding: 6px 10px;

    border-radius: 20px;

    background: #eef2ff;

    border: 1px solid #c7d2fe;

    color: #4f46e5;

    font-size: 10px;

    font-weight: 800;
}


/* Empty chat */

.chat-empty {
    text-align: center;

    background: white;

    border: 1px solid #e5e7eb;

    border-radius: 18px;

    padding: 45px 20px;

    margin-bottom: 15px;
}

.chat-empty-icon {
    width: 48px;
    height: 48px;

    margin: 0 auto 13px auto;

    border-radius: 14px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: linear-gradient(
        135deg,
        #6366f1,
        #8b5cf6
    );

    color: white;

    font-size: 21px;

    font-weight: 800;
}

.chat-empty-title {
    color: #111827;

    font-size: 18px;

    font-weight: 800;

    margin-bottom: 7px;
}

.chat-empty-text {
    color: #64748b;

    font-size: 12px;

    line-height: 1.7;

    max-width: 550px;

    margin: auto;
}


/* Chat messages */

.message-row {
    display: flex;

    gap: 10px;

    align-items: flex-start;

    margin: 13px 0;
}

.user-row {
    justify-content: flex-end;
}

.message-avatar {
    width: 32px;
    height: 32px;

    min-width: 32px;

    border-radius: 9px;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 9px;

    font-weight: 800;
}

.ai-avatar {
    background: linear-gradient(
        135deg,
        #6366f1,
        #8b5cf6
    );

    color: white;
}

.user-avatar {
    background: #111827;

    color: white;

    order: 2;
}

.message {
    max-width: 72%;

    padding: 13px 16px;

    border-radius: 15px;

    font-size: 13px;

    line-height: 1.65;
}

.user-message {
    background: #eef2ff;

    border: 1px solid #e0e7ff;

    color: #312e81;
}

.ai-message {
    background: white;

    border: 1px solid #e5e7eb;

    color: #374151;

    box-shadow:
        0 4px 15px rgba(15, 23, 42, 0.035);
}

.ai-name {
    color: #4f46e5;

    font-size: 10px;

    font-weight: 800;

    margin-bottom: 4px;

    text-transform: uppercase;

    letter-spacing: 0.5px;
}


/* Chat input */

[data-testid="stChatInput"] {
    border-radius: 15px;
}


/* =========================================================
   SOURCES
========================================================= */

.source-card {
    background: white;

    border: 1px solid #e5e7eb;

    border-left: 4px solid #6366f1;

    border-radius: 13px;

    padding: 14px 16px;

    margin-top: 10px;
}

.source-title {
    color: #111827;

    font-size: 12px;

    font-weight: 750;
}

.source-meta {
    color: #64748b;

    font-size: 10px;

    margin-top: 5px;
}


/* =========================================================
   BUTTONS
========================================================= */

.stButton > button {
    border-radius: 10px;

    min-height: 40px;

    border: 1px solid #334155;

    background: #172033;

    color: white;

    font-weight: 650;
}

.stButton > button:hover {
    border-color: #818cf8;

    color: white;

    background: #1e293b;
}


/* =========================================================
   ALERTS
========================================================= */

[data-testid="stAlert"] {
    border-radius: 12px;
}


/* =========================================================
   FOOTER
========================================================= */

.footer {
    text-align: center;

    color: #94a3b8;

    font-size: 10px;

    padding: 30px 0 5px 0;
}


/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 900px) {

    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .welcome-title {
        font-size: 23px;
    }

    .welcome-card {
        padding: 25px;
    }

    .top-header {
        align-items: flex-start;
        gap: 10px;
    }

    .message {
        max-width: 85%;
    }
}

</style>
        """,
        unsafe_allow_html=True
    )