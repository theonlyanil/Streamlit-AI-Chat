import streamlit as st
import json
import google.generativeai as genai

# Set up the API key
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# Function to handle chat with context
def chat_with_context(context, prompt):
    model = genai.GenerativeModel('gemini-2.0-flash-lite')
    chat = model.start_chat(history=[])
    
    response = chat.send_message(f"Context: {context}\n\nHuman: {prompt}")
    return response.text

st.title("Context-Aware Chat App with Gemini")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "context" not in st.session_state:
    st.session_state.context = None

# Context input
st.subheader("Set Context")
input_type = st.selectbox("Choose input type:", ["Text", "JSON"])

col1, col2 = st.columns(2)

with col1:
    if input_type == "Text":
        context_input = st.text_area("Enter your context text:")
    elif input_type == "JSON":
        context_input = st.text_area("Paste your JSON context here:")

with col2:
    if st.button("Set Context"):
        if input_type == "Text":
            st.session_state.context = context_input
            st.session_state.messages = []
            st.success("Context set successfully!")
        elif input_type == "JSON":
            try:
                parsed_json = json.loads(context_input)
                st.session_state.context = json.dumps(parsed_json, indent=2)
                st.session_state.messages = []
                st.success("JSON context set successfully!")
            except json.JSONDecodeError:
                st.error("Invalid JSON format.")

# Chat interface
st.subheader("Chat")
if st.session_state.context is not None:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about the context:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = chat_with_context(st.session_state.context, prompt)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

else:
    st.info("Please set the context (text or JSON) to start chatting.")
