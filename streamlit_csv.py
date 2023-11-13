from api_keys import openai_apikey
import streamlit as st
from dotenv import load_dotenv
import os

from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.llms import OpenAI

def init():
    load_dotenv()

    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY")=="":
        print('OpenAI API key is not set')
        exit(1)
    else:
        print('OpenAI API key is set')

    st.set_page_config(
        page_title="Understand your CSV file",
        page_icon="🤖"
    )

def main():
    init()

    st.header('Understand your CSV file 💾')

    user_csv = st.file_uploader("Upload your csv file", type='csv')

    if user_csv is not None:
        user_question = st.text_input('Ask a question about this csv file:')

        llm = OpenAI(temperature=0, )

        agent = create_csv_agent(llm, user_csv, verbose=True)

        if user_question is not None and user_question != "":
            response = agent.run(user_question)
            st.write(response)

if __name__ == '__main__':
    main()


