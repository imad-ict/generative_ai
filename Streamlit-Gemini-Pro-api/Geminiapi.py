import streamlit as st
import google.generativeai as genai

# Function to read API key from a file
def get_api_key(file_path):
    with open(file_path, 'r') as file:
        return file.readline().strip()

# Configuration for Google Generative AI
GOOGLE_AI_STUDIO = get_api_key('api.txt')  # Path to your api.txt file

genai.configure(api_key=GOOGLE_AI_STUDIO)
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"}
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

chat = model.start_chat(history=[])
def is_code(message):
    # Implement your logic here to determine if a message is code
    # For example, check if it starts with 'import' or contains function definitions
    return message.strip().startswith('import') or 'def ' in message

# Streamlit layout
st.title("Gemini Pro Bot")
st.sidebar.title("Chat")

# Initialize chat history and input in session state if not present
if 'history' not in st.session_state:
    st.session_state.history = []

if 'input' not in st.session_state:
    st.session_state.input = ""

# Chat input
user_input = st.sidebar.text_input("Type your message here:", value=st.session_state.input, key="user_input")

def is_code(message):
    return message.strip().startswith('import') or 'def ' in message
# When the "Send" button is clicked
# Handle the "Send" button click
if st.sidebar.button("Send"):
    if user_input:
        # Send message and get response from AI
        chat.send_message(user_input)
        ai_response = chat.last.text

        # Append user message and AI response to the history
        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("Gemini", ai_response))

        # Reset the input field
        st.session_state.input = ""

# Display chat history with custom styling
for index, (actor, message) in enumerate(st.session_state.history):
    # Determine if the message is from the user or the AI
    if actor == "You":
        # Display user messages in a custom-styled div
        st.markdown(f'''
            <div style="background-color: #fafafa; color: #333333; border-radius: 5px; padding: 10px; margin: 10px 0; font-family: sans-serif;">
                <strong>{actor}:</strong> {message}
            </div>
            ''', unsafe_allow_html=True)
    elif actor == "AI":
        # Display AI messages. If it's code, use st.code, otherwise use custom-styled div
        if is_code(message):
            # Display code with the option to copy it
            st.code(message, language='python')
        else:
            # Display regular AI message
            st.markdown(f'''
                <div style="background-color: #fafafa; color: #333333; border-radius: 5px; padding: 10px; margin: 10px 0; font-family: sans-serif;">
                    <strong>{actor}:</strong> {message}
                </div>
                ''', unsafe_allow_html=True)