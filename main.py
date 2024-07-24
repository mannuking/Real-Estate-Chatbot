import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd
import PyPDF2
import base64
import google.generativeai as genai

st.set_page_config(page_title="Real Estate Assistant", page_icon="🏡", layout="wide")

# Load environment variables and API key
load_dotenv()
api_key = os.getenv("YOUR_API_KEY")
if not api_key:
    st.error("API key not found. Please set up your environment variable correctly.")
    st.stop()

try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Error configuring Google Generative AI: {e}")
    st.stop()

# Function to add background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover;
        padding: 20px;
    }}

    .main {{  /* Added to target the main content area */
        background-color: rgba(255, 255, 255, 0.5);  /* Semi-transparent white background */
        padding: 20px;
        border-radius: 10px; /* Optional rounded corners */
        margin: 80px auto; /* Center the container horizontally */
        margin-bottom: 20px; /* Add some space at the bottom */
        max-width: 900px;  /* Set a maximum width */
        
    }}

    .message {{
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 10px;
        max-width: 70%;
        animation: fadeIn 0.5s ease-in-out;
    }}

    .user-message {{
        background-color: #007bff;
        color: white;
        align-self: flex-end;
        margin-left: auto; 
    }}

    .bot-message {{
        background-color: #e9ecef;
        color: black;
        align-self: flex-start;
    }}

    @keyframes fadeIn {{
        0% {{ opacity: 0; }}
        100% {{ opacity: 1; }}
    }}

    .chat-input {{
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: rgba(255, 255, 255, 0.8);
        padding: 10px;
    }}
    </style>
    """,
        unsafe_allow_html=True
    )

# Add background image
add_bg_from_local('image2.jpg')

# Main Streamlit Application Content
def main():
    st.title("🏡 Real Estate Chatbot 🤖")

    # Check if a page is set in session state
    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        show_home_page()
    elif st.session_state.page == "chatbot":
        show_chatbot_page()

def show_home_page():
    st.header("Welcome to the Real Estate Chatbot")
    st.markdown("Upload a PDF or CSV file containing property details.")

    uploaded_file = st.file_uploader("Upload a PDF or CSV file containing property details")

    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        if st.button("Let's Create the Chatbot"):
            process_uploaded_file(uploaded_file)
            st.session_state.page = "chatbot"
            st.experimental_rerun()

def process_uploaded_file(uploaded_file):
    if uploaded_file.name.endswith('.pdf'):
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        st.session_state.local_data = text
    elif uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        st.session_state.local_data = df.to_csv(index=False)

def show_chatbot_page():
    # st.title("🏡 Real Estate Chatbot 🤖")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display the chat history
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(
                f'<div class="message user-message">{message["content"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="message bot-message">{message["content"]}</div>',
                unsafe_allow_html=True
            )

    st.markdown('</div>', unsafe_allow_html=True)

    user_input = st.text_input("You:", key="chat_input", label_visibility="collapsed", placeholder="Type your message here...", help="Type your message and press Enter to send", on_change=process_input)

def process_input():
    user_input = st.session_state.chat_input
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Generate response using Google Gemini Pro
    prompt = f"""
    You are an advanced real estate assistant with a deep understanding of global real estate knowledge. Your expertise will guide several clients who are in search of a real estate property. 
    Use the following property details provided by the user to answer their questions. 

    Property Details: {st.session_state.get('local_data', 'No property details provided yet.')}

    Conversation History: 
    {[{'User: ' + msg['content'] if msg['role'] == 'user' else 'Bot: ' + msg['content']} for msg in st.session_state.chat_history]} 

    User's latest message: {user_input}

    Please provide a comprehensive, informative, and engaging response based on the property details and global real estate knowledge, considering the conversation history. 
    Always ask questions from the client if in doubt. Don't put out any information that is not verified. 
    """

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        bot_response = response.text
    except Exception as e:
        st.error(f"Error generating chatbot response: {e}")
        bot_response = "Sorry, I couldn't process that."

    st.session_state.chat_history.append({"role": "bot", "content": bot_response})
    # st.experimental_rerun()

if __name__ == "__main__":
    main()
