import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

cookie_path_dir = "./cookies"

st.set_page_config(page_title='⭐️ Hugging Chat 💬💬')
st.title('⭐️ Hugging Chat 💬💬')

with st.sidebar:
    if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
        st.success('HuggingFace Login credentials already provided!', icon='✅')
        hf_email = st.secrets['EMAIL']
        hf_pass = st.secrets['PASS']
    else:
        hf_email = st.text_input('E-mail:')
        hf_pass = st.text_input('Password:', type='password')
        if not (hf_email and hf_pass):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


def generate_response(prompt, email, passwd):
    sign = Login(email, passwd)
    cookies = sign.login()
    sign.saveCookiesToDir(cookie_path_dir)

    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(prompt)

# React to user input
if prompt := st.chat_input("What is up?", disabled=not(hf_pass and hf_email)):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    

    ## generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt, hf_email, hf_pass)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
