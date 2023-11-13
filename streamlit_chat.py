from api_keys import openai_apikey
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage, HumanMessage, AIMessage
)
def init():
    load_dotenv()

    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY")=="":
        print('OpenAI API key is not set')
        exit(1)
    else:
        print('OpenAI API key is set')

    st.set_page_config(
        page_title="Your Own ChatGPT",
        page_icon="🤖"
    )

def main():
    init()

    chat = ChatOpenAI(temperature=0.5)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content='You are a helpful assistant.')
        ]

    st.header('Your own ChatGPT 🤖')


    with st.sidebar:
        user_input = st.text_input("Your message: ", key='user_input')
        st.button('Clear Chat', on_click=clear_chat)
        if user_input:
            #message(user_input, is_user=True)
            st.session_state.messages.append(HumanMessage(content=user_input))
            with st.spinner('Thinking...'):
                response = chat(st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=response.content))
            #message(response.content, is_user=False)

    messages = st.session_state.get("messages", [])
    for i, msg in enumerate(messages[1:]):
        if i%2 == 0:
            message(msg.content, is_user=True, key=str(i)+'_user')
        else:
            message(msg.content, is_user=False, key=str(i)+'_ai')

def clear_chat():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.session_state['user_input'] = ""

if __name__ == '__main__':
    main()


