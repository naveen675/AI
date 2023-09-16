from PyPDF2 import PdfReader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
import streamlit as st
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import VertexAI
from langchain.callbacks import get_openai_callback
import pickle
import time
import os
import google.auth
import dotenv

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="pipeline-399210-dc2d5b9d8250.json"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
os.environ["EMBEDDING_MODEL_NAME"] = "sentence-transformers/all-MiniLM-L6-v2"
credentials, project = google.auth.default()


disable_status = False

pdf = st.file_uploader("Upload your pdf file")
query  = st.text_input("Enter query")


def Train_llm(file):

    embeded = HuggingFaceEmbeddings()
    llm = VertexAI()
    reader = PdfReader(file)
    # st.write(file)

    text = ''
    file_name = file.name[:-4]
    print(file_name)
    if os.path.exists(f"{file_name}.pkl"):
        print("file Exists")
        with open(f"{file_name}.pkl","rb") as f:
            vextorStore = pickle.load(f)
        st.write("Embedings Loaded")
    else:
        for page in reader.pages:
            text += page.extract_text()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap = 20,
            length_function=len

        )

        chunks = splitter.split_text(text)

        len(chunks)
        # print(chunks)
        embeded = HuggingFaceEmbeddings()
        vextorStore = FAISS.from_texts(chunks, embeded)
        st.write("Embedings Loaded")

    chain = load_qa_chain(llm, chain_type = 'stuff')
        
    sys = f'''
    You are a Q and A So you need to answer only for the questions that are related to the ducuments
    that you are trained on. If the information is not in document then Mention "I dont know"
    Please answer to below query
    
    '''
    prompt = f"{sys} \n {query}"
    print(prompt)
    
    
    if query != "" : 
        print("Inside query")
        query =""
        docs = vextorStore.similarity_search(prompt,k=3)
        with get_openai_callback() as cb:
            res = chain.run(input_documents=docs, question=prompt)
            print(cb)
        st.write(res)
        



    







if pdf is not None:
   
    print("pdf")
    Train_llm(pdf)
    


    