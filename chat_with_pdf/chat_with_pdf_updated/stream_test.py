from PyPDF2 import PdfReader
from langchain.embeddings import VertexAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
import streamlit as st
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import VertexAI

import os
import google.auth

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="genia-data-pipe-9398703f765d.json"
credentials, project = google.auth.default()
llm = VertexAI(model_name="text-bison@001",
        max_output_tokens=256,
        temperature=0.1,
        top_p=0.8,
        top_k=40,
        verbose=True,)

embeded = VertexAIEmbeddings()

prompt  = st.text_input("Enter the input")

def response(file):

    reader = PdfReader(file)

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
    embeded = VertexAIEmbeddings()
    vextorStore = FAISS.from_texts(chunks, embeded)

    chain = load_qa_chain(llm, chain_type = 'stuff')

    query = "Who are the authors of this article  Using Lightweight Formal Methods to Validate a Key-Value Storage Node in Amazon S3"
    docs = vextorStore.similarity_search(query)
    return chain.run(input_documents=docs, question=query)

    

def get_response(prompt):

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="genia-data-pipe-9398703f765d.json"
    credentials, project = google.auth.default()

    url = "Amazon Paper of Month.pdf"
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
    loader = PyPDFLoader("https://icseindia.org/document/sample.pdf")
    documents = loader.load()
    chunks = text_splitter.split_documents(documents)
    print(f"# of documents = {len(docs)}")
    # splitter = CharacterTextSplitter(
    # separator = "\n",
    # chunk_size=4000,
    # chunk_overlap = 200,
    # length_function=len)
    # chunks = splitter.split_documents(documents)
    print(f"# of documents = {len(chunks)}")

    len(chunks)
    embeded_doc = FAISS.from_texts(chunks, embeded)
    chain = load_qa_chain(llm, chain_type = 'stuff')
    query = "Who are the authors of this article  YOLOv7: Trainable bag-of-freebies sets new state-of-the-art for real-time object detectors"
    docs = embeded_doc.similarity_search(query)
    res = chain.run(input_documents=docs, question=query)
    print(res)








if prompt:

    res = response(prompt)
    st.write(res)