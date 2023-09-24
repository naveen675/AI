from langchain.vectorstores import Pinecone
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub,VertexAI
import os
from langchain.chat_models import ChatVertexAI
import requests
from bs4 import BeautifulSoup
import re
import google.auth
import pinecone
from langchain.chains.question_answering import load_qa_chain

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_ENV = os.environ.get('PINECONE_ENV')
vectorstore = pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
embeddings = HuggingFaceEmbeddings()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="pipeline-399210-9d5c4c0d8b7d.json"
credentials, project = google.auth.default()


url = "https://www.who.int/emergencies/disease-outbreak-news/item/2023-DON488"

def preprocess_text(text):
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text


def get_text_from_link(link):

    try:
     
    
        resource_response = requests.get(link)

            # Parse the HTML content of the resource page
        print(resource_response)

    
         

        resource_soup = BeautifulSoup(resource_response.text, "html.parser")

            # Extract relevant text content (customize as needed)
        resource_text = resource_soup.get_text()
        resource_text = preprocess_text(resource_text)
        # print(resource_text)
        return resource_text
        #print(resource_text)

    except Exception as e :
         print(f"! NOT WORKING  {link} ") 

def embed(chunks):
     
    index_name ="covid19-embeddings" 
    # print(len(chunks.split()))
    dimension = len(embeddings.embed_documents(chunks))
    # print(len(dimension))

    if index_name not in pinecone.list_indexes():
    # we create a new index
        pinecone.create_index(
        name=index_name,
        dimension=768,
        )

    vectorstore=Pinecone.from_texts(chunks, embeddings, index_name=index_name)
    return vectorstore
    
def get_text_chunks(text):
    

    chunk_size = 100
    overlap = 20
    chunks = []

    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

    # for i, chunk in enumerate(chunks):
    #     print(f"Chunk {i + 1}:\n{chunk}\n")
    return chunks

     

# text = get_text_from_link(url)
# chunks = get_text_chunks(text)
# # print(len(chunks))
# vectorstore = embed(chunks)
# Perform a similarity search in Pinecone

llm = VertexAI()
user_query ="How the Cholera is infected"
index = pinecone.Index("covid19-embeddings")
vectorstore = Pinecone(index, embeddings.embed_query, "text")
docs = vectorstore.similarity_search(user_query)
chain = load_qa_chain(llm, chain_type = 'stuff')
print(chain.run(input_documents=docs, question=user_query))
# results = vectorstore.query(index_name="web_search_embeddings", query_vector=user_query_embedding, top_k=1)
# Retrieve the content associated with the top results
# index = pinecone.Index("covid19-embeddings")
# vectorstore = Pinecone(index, embeddings.embed_query, "text")

# results = vectorstore.similarity_search(user_query,k=1)
# print(results)





