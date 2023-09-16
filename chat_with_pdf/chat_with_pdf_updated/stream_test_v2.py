from PyPDF2 import PdfReader
from langchain.embeddings import VertexAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
import streamlit as st
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import VertexAI
import time
import os
import google.auth

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="genia-data-pipe-70fb62581547.json"
credentials, project = google.auth.default()
llm = VertexAI(model_name="text-bison@001",
        max_output_tokens=256,
        temperature=0.1,
        top_p=0.8,
        top_k=40,
        verbose=True,)

disable_status = False

pdf = st.file_uploader("Upload your pdf file",disabled=disable_status)

def Train_llm(file):

    embeded = VertexAIEmbeddings()
    reader = PdfReader(file)
    # st.write(file)

    pdf_data = ''
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pdf_data += text

    splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size=4000,
        chunk_overlap = 200,
        length_function=len

    )

    chunks = splitter.split_text(pdf_data)

    len(chunks)
    # print(chunks)
    embeded = VertexAIEmbeddings()
    vextorStore = FAISS.from_texts(chunks, embeded)

    chain = load_qa_chain(llm, chain_type = 'stuff')

    #query = "Who are the authors of this article  Using Lightweight Formal Methods to Validate a Key-Value Storage Node in Amazon S3"
    query = "What is the name mentioned in Deeplearning.AI"
    
    
    if chain : 

        query  = st.text_input("Enter query")
        docs = vextorStore.similarity_search(query)
        return chain.run(input_documents=docs, question=query)

def get_query_response(vextorStore,query):

    docs = vextorStore.similarity_search(query)
    print("inside query")
    chain = load_qa_chain(llm, chain_type = 'stuff')
    return chain.run(input_documents=docs, question=query)






query=""
file_name = ""
if pdf:
    file_name = pdf
    response = Train_llm(file_name)
    if response:
        st.write(response)


    