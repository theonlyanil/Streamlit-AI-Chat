import streamlit as st
import json
import google.generativeai as genai
from stealthkit import StealthSession

ss = StealthSession()

# Set up the API key
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

# Function to handle chat with context
def chat_with_context(context, prompt):
    model = genai.GenerativeModel('gemini-2.0-flash-lite')
    chat = model.start_chat(history=[])
    
    response = chat.send_message(f"Context: {context}\n\nHuman: {prompt}")
    return response.text

st.title("Chat with Reddit Post")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "context" not in st.session_state:
    st.session_state.context = None

# Reddit post URL input
st.subheader("Enter Reddit Post URL")
reddit_url = st.text_input("Reddit Post URL (e.g., https://www.reddit.com/r/programming/comments/18yzp1c/what_are_the_most_important_skills_for_a_junior/)")

if st.button("Fetch Reddit Data"):
    if reddit_url:
        try:
            json_url = reddit_url.rstrip('/') + ".json"
            ss.fetch_cookies("https://www.reddit.com")
            response = ss.get(json_url)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            data = response.json()

            # Extract relevant information from Reddit JSON
            post_data = data[0]['data']['children'][0]['data']
            comments_data = [comment['data']['body'] for comment in data[1]['data']['children'] if 'data' in comment and 'body' in comment['data']]

            context_data = {
                "title": post_data.get('title', 'No Title'),
                "selftext": post_data.get('selftext', 'No Selftext'),
                "comments": comments_data
            }

            st.session_state.context = json.dumps(context_data, indent=2)
            st.session_state.messages = []
            st.success("Reddit data fetched and set as context!")

        except Exception as e:
            st.error(f"Error fetching Reddit data: {e}")
        except json.JSONDecodeError:
            st.error("Invalid JSON response from Reddit.")
        except KeyError:
            st.error("Error parsing Reddit JSON. Unexpected data structure.")
    else:
        st.warning("Please enter a Reddit URL.")

# Chat interface
st.subheader("Chat")
if st.session_state.context is not None:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about the Reddit post:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = chat_with_context(st.session_state.context, prompt)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

else:
    st.info("Please enter a Reddit Post URL and click 'Fetch Reddit Data' to start chatting.")