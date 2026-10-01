
import streamlit as st


def display_chat():

    st.subheader("Ask a Question")

    # Create chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    question = st.chat_input(
        "Ask a question about the document..."
    )

    if question:

        # Display user question
        with st.chat_message("user"):
            st.write(question)

        # Save user question
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        # Temporary response
        answer = "Waiting for backend response..."

        # Display assistant response
        with st.chat_message("assistant"):
            st.write(answer)

        # Save assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })
        