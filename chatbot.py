import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure API - add your key in .env file
genai.configure(api_key="AIzaSyCBATZFHWzLiHnsN_CKUV0Nj9f8sXjNLYU")

def chatbot():
    st.title("🎨 Sanskriti Sutra AI Assistant")
    st.caption("Your guide to Indian art, culture, tourism, and history")
    """Streamlit chatbot function restricted to art, culture, tourism, and history"""
    # Initialize model
    if "model" not in st.session_state:
        st.session_state.model = genai.GenerativeModel(
            model_name="models/gemini-1.5-flash"
        )
    
    # Initialize chat session with system instructions
    if "chat" not in st.session_state:
        system_instruction = (
            "You are a specialized assistant for art, culture, tourism, and history. "
            "Follow these rules strictly:\n"
            "1. Only answer questions about: \n"
            "   - Art (artists, movements, techniques)\n"
            "   - Cultural traditions, festivals, customs\n"
            "   - Tourism destinations, landmarks, travel tips\n"
            "   - Historical events, figures, civilizations\n"
            "2. For any other topics, respond ONLY with: "
            "'I can only answer questions about art, culture, tourism, or history.'\n"
            "3. Never justify or explain the restriction\n"
            "4. Be engaging and informative for valid topics"
        )
        st.session_state.chat = st.session_state.model.start_chat(history=[
            {"role": "user", "parts": [system_instruction]},
            {"role": "model", "parts": ["I understand. I will only answer questions about art, culture, tourism, and history."]}
        ])
    
    # Initialize messages
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! Ask me about art, culture, tourism, or history."}
        ]
    
    # Display messages
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    
    # Handle user input
    if prompt := st.chat_input("Ask about art, culture, tourism, or history"):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        try:
            # Get response
            response = st.session_state.chat.send_message(prompt)
            reply = response.text
            
            # Add assistant message to history
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.chat_message("assistant").write(reply)
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            st.chat_message("assistant").write(error_msg)

# Run the chatbot
# if __name__ == "__main__":
#     chatbot()