import streamlit as st

def main():
    st.set_page_config(
        page_title="AI Chat Hub",
        page_icon="🤖",
        layout="wide",
    )

    st.title("Welcome to the AI Chat Hub! 🤖")

    st.markdown(
        """
        Explore a collection of AI-powered chat applications. Choose a chat app from the sidebar to get started.

        We use Google's gemini chat interface for your custom needs.
        
        **Instructions:**

        1.  Select an app from the sidebar.
        2.  Start chatting!

        **Note:** Some apps may require API keys. Please refer to the app's instructions for details.

        **Security Notice:** Please be aware that when using publicly available apps, do not share sensitive information.
        """
    )

    st.sidebar.header("Select an App")
    st.sidebar.markdown("""
    * [Gemini Chat](gemini_chat)
    * [Reddit Chat](reddit_chat)

    """)

if __name__ == "__main__":
    main()