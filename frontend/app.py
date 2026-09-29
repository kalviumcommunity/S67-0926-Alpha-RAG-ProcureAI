import streamlit as st

st.set_page_config(
    page_title="Procurement Assistant",
    page_icon="📄"
)

st.title("📄 Procurement Assistant")

st.write("Upload a procurement document and ask questions about it.")

uploaded_file = st.file_uploader(
    "Upload your document",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:
    st.success(f"{uploaded_file.name} uploaded successfully!")

question = st.chat_input("Ask a question about the document...")

if question:
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        st.write("Waiting for backend...")