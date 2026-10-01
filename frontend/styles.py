import streamlit as st


def load_css():
    st.markdown(
        """
        <style>

        /* ==============================
           GLOBAL
        ============================== */

        .stApp {
            background: #f6f8fc;
        }

        .main .block-container {
            max-width: 1450px;
            padding-top: 1.5rem;
            padding-bottom: 3rem;
            padding-left: 2.5rem;
            padding-right: 2.5rem;
        }

        /* Hide Streamlit default header */
        header[data-testid="stHeader"] {
            background: transparent;
        }

        /* ==============================
           SIDEBAR
        ============================== */

        section[data-testid="stSidebar"] {
            background: #111827;
            border-right: 1px solid #1f2937;
        }

        section[data-testid="stSidebar"] > div {
            background: #111827;
        }

        section[data-testid="stSidebar"] * {
            color: #f9fafb;
        }

        .sidebar-brand {
            padding: 10px 5px 25px 5px;
        }

        .sidebar-logo {
            width: 42px;
            height: 42px;
            border-radius: 12px;
            background: linear-gradient(
                135deg,
                #6366f1,
                #8b5cf6
            );
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 21px;
            font-weight: 800;
            color: white;
            margin-bottom: 12px;
        }

        .sidebar-brand-name {
            font-size: 20px;
            font-weight: 800;
            color: white;
            margin-bottom: 2px;
        }

        .sidebar-brand-subtitle {
            font-size: 12px;
            color: #9ca3af;
        }

        .sidebar-section {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #6b7280;
            font-weight: 700;
            margin-top: 20px;
            margin-bottom: 10px;
        }

        .sidebar-item {
            padding: 10px 12px;
            border-radius: 10px;
            margin-bottom: 4px;
            color: #d1d5db;
            font-size: 14px;
        }

        .sidebar-item-active {
            background: #1f2937;
            color: white;
        }

        .sidebar-footer {
            margin-top: 30px;
            padding: 15px;
            background: #1f2937;
            border: 1px solid #374151;
            border-radius: 14px;
        }

        .sidebar-footer-title {
            font-size: 12px;
            font-weight: 700;
            color: white;
            margin-bottom: 5px;
        }

        .sidebar-footer-text {
            font-size: 11px;
            color: #9ca3af;
            line-height: 1.5;
        }

        /* ==============================
           TOP BAR
        ============================== */

        .topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 8px 0 22px 0;
            border-bottom: 1px solid #e5e7eb;
            margin-bottom: 25px;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .brand-logo {
            width: 42px;
            height: 42px;
            border-radius: 12px;
            background: linear-gradient(
                135deg,
                #6366f1,
                #8b5cf6
            );
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 20px;
            font-weight: 800;
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.25);
        }

        .brand-name {
            font-size: 20px;
            font-weight: 800;
            color: #111827;
        }

        .brand-subtitle {
            font-size: 11px;
            color: #6b7280;
            margin-top: 1px;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 13px;
            border-radius: 30px;
            background: #ecfdf5;
            color: #047857;
            border: 1px solid #a7f3d0;
            font-size: 12px;
            font-weight: 700;
        }

        .status-dot {
            width: 7px;
            height: 7px;
            background: #10b981;
            border-radius: 50%;
        }

        /* ==============================
           HERO
        ============================== */

        .hero {
            background: linear-gradient(
                135deg,
                #111827 0%,
                #1e1b4b 55%,
                #312e81 100%
            );
            border-radius: 24px;
            padding: 42px;
            color: white;
            margin-bottom: 25px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 18px 45px rgba(17, 24, 39, 0.15);
        }

        .hero::after {
            content: "";
            position: absolute;
            width: 300px;
            height: 300px;
            border-radius: 50%;
            background: rgba(139, 92, 246, 0.18);
            right: -80px;
            top: -120px;
        }

        .hero-label {
            display: inline-block;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 6px 11px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.7px;
            text-transform: uppercase;
            margin-bottom: 15px;
        }

        .hero-title {
            font-size: 36px;
            font-weight: 850;
            letter-spacing: -1px;
            margin: 0 0 12px 0;
            position: relative;
            z-index: 2;
        }

        .hero-text {
            font-size: 15px;
            line-height: 1.7;
            color: #d1d5db;
            max-width: 700px;
            position: relative;
            z-index: 2;
        }

        /* ==============================
           STAT CARDS
        ============================== */

        .stat-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 18px;
            padding: 20px;
            min-height: 125px;
            box-shadow: 0 5px 18px rgba(17, 24, 39, 0.04);
            transition: 0.2s ease;
        }

        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(17, 24, 39, 0.08);
        }

        .stat-icon {
            width: 38px;
            height: 38px;
            border-radius: 10px;
            background: #eef2ff;
            color: #4f46e5;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            margin-bottom: 12px;
        }

        .stat-label {
            font-size: 12px;
            color: #6b7280;
            margin-bottom: 4px;
        }

        .stat-value {
            font-size: 25px;
            font-weight: 800;
            color: #111827;
        }

        /* ==============================
           SECTION
        ============================== */

        .section-title {
            font-size: 20px;
            font-weight: 800;
            color: #111827;
            margin-top: 28px;
            margin-bottom: 4px;
        }

        .section-description {
            color: #6b7280;
            font-size: 13px;
            margin-bottom: 16px;
        }

        /* ==============================
           DOCUMENT CARD
        ============================== */

        .document-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 18px;
            padding: 18px;
            margin-bottom: 12px;
            box-shadow: 0 5px 18px rgba(17, 24, 39, 0.04);
        }

        .document-icon {
            width: 42px;
            height: 42px;
            border-radius: 11px;
            background: #eef2ff;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #4f46e5;
            font-size: 19px;
            margin-bottom: 10px;
        }

        .document-name {
            font-size: 14px;
            font-weight: 750;
            color: #111827;
            word-break: break-word;
        }

        .document-meta {
            font-size: 11px;
            color: #6b7280;
            margin-top: 4px;
        }

        .document-status {
            display: inline-block;
            margin-top: 10px;
            padding: 5px 9px;
            border-radius: 20px;
            background: #ecfdf5;
            color: #047857;
            font-size: 10px;
            font-weight: 700;
        }

        /* ==============================
           CHAT
        ============================== */

        .chat-user {
            background: #eef2ff;
            border: 1px solid #e0e7ff;
            border-radius: 16px;
            padding: 15px 18px;
            margin: 10px 0;
            color: #312e81;
            line-height: 1.6;
        }

        .chat-ai {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 16px;
            padding: 18px;
            margin: 10px 0;
            color: #374151;
            line-height: 1.7;
            box-shadow: 0 5px 18px rgba(17, 24, 39, 0.04);
        }

        .ai-label {
            font-size: 11px;
            color: #4f46e5;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.7px;
            margin-bottom: 8px;
        }

        /* ==============================
           SOURCE CARD
        ============================== */

        .source-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-left: 4px solid #6366f1;
            border-radius: 13px;
            padding: 14px 16px;
            margin-bottom: 10px;
        }

        .source-title {
            font-size: 13px;
            font-weight: 750;
            color: #111827;
        }

        .source-meta {
            font-size: 11px;
            color: #6b7280;
            margin-top: 5px;
        }

        /* ==============================
           CAPABILITIES
        ============================== */

        .capability-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 16px;
            padding: 18px;
            height: 100%;
            box-shadow: 0 5px 18px rgba(17, 24, 39, 0.03);
        }

        .capability-icon {
            font-size: 20px;
            margin-bottom: 10px;
        }

        .capability-title {
            font-size: 14px;
            font-weight: 750;
            color: #111827;
            margin-bottom: 5px;
        }

        .capability-text {
            font-size: 12px;
            color: #6b7280;
            line-height: 1.5;
        }

        /* ==============================
           BUTTONS
        ============================== */

        .stButton > button {
            border-radius: 11px;
            border: 1px solid #e5e7eb;
            font-weight: 650;
            min-height: 42px;
        }

        .stButton > button:hover {
            border-color: #6366f1;
            color: #4f46e5;
        }

        /* ==============================
           FILE UPLOADER
        ============================== */

        [data-testid="stFileUploader"] {
            background: white;
            border: 2px dashed #c7d2fe;
            border-radius: 18px;
            padding: 8px;
        }

        [data-testid="stFileUploader"]:hover {
            border-color: #818cf8;
            background: #fafaff;
        }

        /* ==============================
           CHAT INPUT
        ============================== */

        [data-testid="stChatInput"] {
            border-radius: 15px;
        }

        /* ==============================
           TEXT INPUT
        ============================== */

        .stTextInput > div > div > input {
            border-radius: 12px;
            border: 1px solid #e5e7eb;
        }

        .stTextInput > div > div > input:focus {
            border-color: #6366f1;
            box-shadow: 0 0 0 1px #6366f1;
        }

        /* ==============================
           SELECT BOX
        ============================== */

        .stSelectbox > div > div {
            border-radius: 12px;
        }

        /* ==============================
           METRIC
        ============================== */

        [data-testid="stMetric"] {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 16px;
            padding: 15px;
        }

        /* ==============================
           EXPANDER
        ============================== */

        [data-testid="stExpander"] {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
        }

        /* ==============================
           ALERTS
        ============================== */

        [data-testid="stAlert"] {
            border-radius: 13px;
        }

        /* ==============================
           FOOTER
        ============================== */

        .footer {
            text-align: center;
            padding: 25px 0 10px 0;
            color: #9ca3af;
            font-size: 11px;
        }

        /* ==============================
           RESPONSIVE
        ============================== */

        @media (max-width: 900px) {

            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .hero-title {
                font-size: 24px;
            }

            .hero {
                padding: 25px;
            }

            .topbar {
                flex-direction: column;
                align-items: flex-start;
                gap: 12px;
            }

            .stat-card {
                min-height: 105px;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
    )