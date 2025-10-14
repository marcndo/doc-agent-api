import streamlit as st
import requests
import time

# Configuration
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Doc Q&A", page_icon="📄")
st.title("📄 Smart Document & Web Q&A")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- NEW: Updated Sidebar for Document and URL ---
with st.sidebar:
    st.header("Add a Source")

    # Option 1: File Uploader
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf", key="file_uploader")

    # Option 2: URL Input
    url_input = st.text_input("Or enter a Web URL", key="url_input")

    # Process Button
    if st.button("Process Source"):
        if uploaded_file is None and not url_input:
            st.warning("Please upload a file or enter a URL.")
        elif uploaded_file and url_input:
            st.warning("Please provide either a file or a URL, not both.")
        else:
            with st.spinner('Processing source...'):
                try:
                    # Logic to send the correct request to the backend
                    if uploaded_file:
                        files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'application/pdf')}
                        response = requests.post(f"{API_URL}/process/", files=files)
                    else:  # If not a file, it must be a URL
                        data = {'url': url_input}
                        response = requests.post(f"{API_URL}/process/", data=data)

                    if response.status_code == 200:
                        st.success("Source processed successfully!")
                        st.session_state.messages = []  # Clear chat on new source
                        # Clear the widgets after successful processing
                        st.session_state.file_uploader = None
                        st.session_state.url_input = ""
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")

                except requests.exceptions.RequestException as e:
                    st.error(f"Could not connect to the backend: {e}")

# --- Main Chat Interface (No changes needed here) ---
st.header("Chat with your Document or URL")

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask a question about your source..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        with st.spinner("Thinking..."):
            try:
                response = requests.post(f"{API_URL}/query/", data={"query_text": prompt})
                if response.status_code == 200:
                    full_response = response.json().get("answer", "No answer found.")
                else:
                    full_response = f"Error from API: {response.json().get('detail', 'Unknown error')}"
            except requests.exceptions.RequestException as e:
                full_response = f"Could not connect to the backend: {e}"

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
