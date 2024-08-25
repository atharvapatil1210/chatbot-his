# Install required packages
# !pip install openai streamlit requests

import requests
import streamlit as st
#import nltk
#nltk.download('punkt')

RAPIDAPI_KEY = "dc10ba3fa2mshb5b796ba35c4fe4p161161jsn6a0ba268f2ec"
RAPIDAPI_HOST = "chatgpt-42.p.rapidapi.com"

def chat_with_gpt(prompt):
    # No tokenization
    tokens_used = len(prompt.split())  # Simple token count

    if prompt.lower().startswith(("what", "how")):
        return "This is a placeholder response.", tokens_used  # Simple placeholder response
    else:
        url = f"https://{RAPIDAPI_HOST}/conversationgpt4-2"
        headers = {
            "Content-Type": "application/json",
            "x-rapidapi-host": RAPIDAPI_HOST,
            "x-rapidapi-key": RAPIDAPI_KEY
        }
        data = {
            "messages": [{"role": "user", "content": prompt}],
            "system_prompt": "",
            "temperature": 0.9,
            "top_k": 5,
            "top_p": 0.9,
            "max_tokens": 256,
            "web_access": False
        }
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()

        if 'result' in response_json:
            return response_json['result'], response_json.get('usage', {}).get('total_tokens', 0)
        else:
            return "Error: Unable to get response from ChatGPT-4", 0

def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state["history"] = []
    if "token_usage" not in st.session_state:
        st.session_state["token_usage"] = 0

def on_click_callback():
    human_prompt = st.session_state.human_prompt
    response, tokens_used = chat_with_gpt(human_prompt)
    st.session_state.history.append(("user", human_prompt))
    st.session_state.history.append(("ai", response))
    st.session_state.token_usage += tokens_used

initialize_session_state()

st.title('Hello Student...👩🏻‍💻📓✍🏻💡')  # Title

chat_placeholder = st.container()
promptholder = st.form("chat-form")
credit_card_placeholder = st.empty()

# CSS for styling messages
st.markdown("""
    <style>
    .user-message {
        background-color: #000000;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: left;
        max-width: 70%;
    }
    .ai-message {
        background-color: #000000;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: right;
        max-width: 70%;
        margin-left: auto;
    }
    .avatar-user {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 10px;
        float: left;
    }
    .avatar-ai {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-left: 10px;
        float: right;
    }
    </style>
""", unsafe_allow_html=True)

# Inject the custom JavaScript
st.markdown("""
    <script>
    document.addEventListener("DOMContentLoaded", function() {
        const customButton = document.getElementById("custom-submit-btn");
        if (customButton) {
            customButton.addEventListener("click", function() {
                document.querySelector('form').dispatchEvent(new Event('submit', { bubbles: true }));
            });
        }
    });
    </script>
""", unsafe_allow_html=True)

with chat_placeholder:
    for sender, message in st.session_state.history:
        if sender == "user":
            st.markdown(f'<div class="user-message"><img src="avatars/user-avatar.png" class="avatar-user">{message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-message"><img src="avatars/ai-avatar.png" class="avatar-ai">{message}</div>', unsafe_allow_html=True)

with promptholder:
    cols = st.columns((6, 1))
    human_prompt = cols[0].text_input(
        "Chat",
        placeholder="Ask me anything related to Rajasthan Colleges",
        label_visibility="collapsed",
        key="human_prompt"
    )
    cols[1].form_submit_button(
        "Send",
        type="primary",
        on_click=on_click_callback
    )

    # Add a custom submit button
    st.markdown('<button id="custom-submit-btn">Custom Submit</button>', unsafe_allow_html=True)

# Display token usage
st.write(f"Total tokens used: {st.session_state.token_usage}")
