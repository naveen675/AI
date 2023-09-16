from PyPDF2 import PdfReader
from langchain.embeddings import VertexAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
import streamlit as st
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import VertexAI
import pickle
import time
import os
import google.auth

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="genia-data-pipe-70fb62581547.json"
credentials, project = google.auth.default()
llm = VertexAI()

disable_status = False

pdf = st.file_uploader("Upload your pdf file",disabled=disable_status)


def Train_llm(file):

    embeded = VertexAIEmbeddings()
    reader = PdfReader(file)
    st.write(file)

    text = ''
    file_name = file.name
    if os.path.exists(file_name):
        with open(f"{file_name}.pkl","rb") as f:
            vectorStore = pickle.load(f)
        st.write("Embedings Loaded")
        return vectorStore
    else:
        for page in reader.pages:
            text += page.extract_text()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            chunk_overlap = 20,
            length_function=len

        )

        chunks = splitter.split_text(text)

        len(chunks)
        # print(chunks)
        embeded = VertexAIEmbeddings()
        vextorStore = FAISS.from_texts(chunks, embeded)
        st.write("Embedings Loaded")
        return vextorStore

    # chain = load_qa_chain(llm, chain_type = 'stuff')

    # #query = "Who are the authors of this article  Using Lightweight Formal Methods to Validate a Key-Value Storage Node in Amazon S3"
    # query = "What is the name mentioned in Deeplearning.AI"
    
    
    # if chain : 

    #     query  = st.text_input("Enter query")
    #     docs = vextorStore.similarity_search(query)
    #     return chain.run(input_documents=docs, question=query)

def get_query_response(vextorStore,query):

    docs = vextorStore.similarity_search(query)
    print("inside query")
    chain = load_qa_chain(llm, chain_type = 'stuff')
    return chain.run(input_documents=docs, question=query)

    

# def get_response(prompt):

#     os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="genia-data-pipe-9398703f765d.json"
#     credentials, project = google.auth.default()

#     url = "Amazon Paper of Month.pdf"
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
#     loader = PyPDFLoader("https://icseindia.org/document/sample.pdf")
#     documents = loader.load()
#     chunks = text_splitter.split_documents(documents)
#     print(f"# of documents = {len(docs)}")
#     # splitter = CharacterTextSplitter(
#     # separator = "\n",
#     # chunk_size=4000,
#     # chunk_overlap = 200,
#     # length_function=len)
#     # chunks = splitter.split_documents(documents)
#     print(f"# of documents = {len(chunks)}")

#     len(chunks)
#     embeded_doc = FAISS.from_texts(chunks, embeded)
#     chain = load_qa_chain(llm, chain_type = 'stuff')
#     query = "Who are the authors of this article  YOLOv7: Trainable bag-of-freebies sets new state-of-the-art for real-time object detectors"
#     docs = embeded_doc.similarity_search(query)
#     res = chain.run(input_documents=docs, question=query)
#     print(res)






query=""
file_name = ""
if pdf is not None:
    file_name = pdf
    disable_status=True
    pdf=""
    print("pdf")
    vectorStore = Train_llm(file_name)
    query  = st.text_input("Enter query")

if query:
        
    print("hello")
    response = get_query_response(vectorStore,query)
        
    st.write(response)
    