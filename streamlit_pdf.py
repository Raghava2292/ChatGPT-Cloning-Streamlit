from api_keys import openai_apikey
import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback

def init():
    load_dotenv()

    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY")=="":
        print('OpenAI API key is not set')
        exit(1)
    else:
        print('OpenAI API key is set')

    st.set_page_config(
        page_title="Understand your PDF file",
        page_icon="🤖"
    )

def main():
    init()

    st.header('Understand your PDF file 💾')

    # Uploading the PDF file
    user_pdf = st.file_uploader("Upload your pdf file", type='pdf')

    # Extracting the text from the file
    if user_pdf is not None:
        pdf_reader = PdfReader(user_pdf)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()

        # splitting the text data into chunks of text
        text_splitter = CharacterTextSplitter(
            separator='\n',
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

        chunks = text_splitter.split_text(text)

        # creating word embeddings from the chunks of text and making a knowledge base to refer to
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)

       
        user_question = st.text_input('Ask a question about the content in this PDF file:')

        llm = OpenAI(temperature=0)

        if user_question is not None and user_question != "":
            docs = knowledge_base.similarity_search(user_question)

            chain = load_qa_chain(llm, chain_type='stuff')
            with get_openai_callback() as cb:
                response = chain.run(input_documents = docs, question = user_question)
                print(cb)

            st.write(response)

if __name__ == '__main__':
    main()


