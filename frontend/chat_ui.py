import streamlit as st


def display_chat():

    # =====================================================
    # CHAT HEADER
    # =====================================================

    st.markdown(
        """
<div class="chat-header">
    <div>
        <div class="chat-title">
            Ask ProcureAI
        </div>

        <div class="chat-subtitle">
            Ask questions about your uploaded procurement documents
        </div>
    </div>

    <div class="chat-badge">
        AI POWERED
    </div>
</div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # SESSION STATE
    # =====================================================

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # =====================================================
    # EMPTY CHAT
    # =====================================================

    if not st.session_state.messages:

        st.markdown(
            """
<div class="chat-empty">

    <div class="chat-empty-icon">
        ✦
    </div>

    <div class="chat-empty-title">
        What would you like to know?
    </div>

    <div class="chat-empty-text">
        Ask about contracts, pricing, suppliers,
        policies, terms, deadlines or anything
        inside your procurement documents.
    </div>

</div>
            """,
            unsafe_allow_html=True
        )

    # =====================================================
    # CHAT HISTORY
    # =====================================================

    for message in st.session_state.messages:

        if message["role"] == "user":

            st.markdown(
                f"""
<div class="message-row user-row">

    <div class="message-avatar user-avatar">
        YOU
    </div>

    <div class="message user-message">
        {message["content"]}
    </div>

</div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
<div class="message-row">

    <div class="message-avatar ai-avatar">
        ✦
    </div>

    <div class="message ai-message">

        <div class="ai-name">
            ProcureAI
        </div>

        {message["content"]}

    </div>

</div>
                """,
                unsafe_allow_html=True
            )

    # =====================================================
    # CHAT INPUT
    # =====================================================

    question = st.chat_input(
        "Ask anything about your procurement documents..."
    )

    if question:

        # Increase question count
        st.session_state.questions = (
            st.session_state.get("questions", 0) + 1
        )

        # Save user question
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        # =================================================
        # TEMPORARY BACKEND RESPONSE
        # =================================================
        #
        # Person 1's RAG API will replace this section.
        #

        answer = (
            "I received your question. "
            "The RAG backend will provide the grounded "
            "answer and supporting document sources here."
        )

        # Save AI response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.rerun()