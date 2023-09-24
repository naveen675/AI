from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub,VertexAI
import os
from langchain.chat_models import ChatVertexAI
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup

import re

import pinecone

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_ENV = os.environ.get('PINECONE_ENV')
# print(PINECONE_API_KEY)
# print(PINECONE_ENV)
conn = pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
index_name = "covid19-embeddings"
# embedding_dimension = 100
# pinecone.create_index(index_name, dimension=100)
# print(conn)

import requests
from bs4 import BeautifulSoup

def get_urls_WHO():

    links_list =[]

    url = "https://www.who.int/emergencies/disease-outbreak-news"


    response = requests.get(url)


    if response.status_code == 200:
   
        soup = BeautifulSoup(response.text, "html.parser")

        links = soup.find_all("a")


        for link in links:
            href = link.get("href")
        
            if "https" in href:
                print(href)
                links_list.append(link)

        return links_list

    else:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"


def preprocess_text(text):
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

def get_text_from_link(link):
     
     
    resource_response = requests.get(link)

        # Parse the HTML content of the resource page
    resource_soup = BeautifulSoup(resource_response.text, "html.parser")

        # Extract relevant text content (customize as needed)
    resource_text = resource_soup.get_text()
    preprocess = preprocess_text(resource_text)
    return resource_text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=20, length_function=len)
    chunks = text_splitter.split_text(text)
    return chunks

# def get_vector_store(text_chunks):
#     embeddings=HuggingFaceEmbeddings()
#     #embeddings=HuggingFaceEmbeddings(model_name = embedding_model_name)
#     vectorstore = FAISS.from_texts(text_chunks, embedding=embeddings)
#     return vectorstore

     
     
def create_and_store_embeddings(url_list):

    resource_links = url_list
    embeddings=HuggingFaceEmbeddings()

    for url in resource_links:

        raw_text = get_text_from_link(url)
        
        # Preprocess the text
        cleaned_text = preprocess_text(raw_text)

        text_chunks = get_text_chunks(cleaned_text)

        document_id = url  # You can use the URL as the document ID in this example
        pinecone.index(index_name="covid19_embeddings", ids=[document_id], embeddings=[embeddings])

    # Close the Pinecone connection when done
    pinecone.deinit()


get_urls_WHO()



