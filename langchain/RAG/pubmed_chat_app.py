from flask import Flask, request, jsonify, render_template, redirect, url_for
import requests
import os
from langchain.llms import VertexAI
from langchain.prompts import PromptTemplate
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import VertexAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain

app = Flask(__name__)

vectorstore = None

llm = VertexAI()

def simulate_llm_model(query):
    # global llm

    template = """if you dont have exact answer for the Question: {query}, then send Answer as False

    Answer: if answer is accurate then send the answer or else send as Flase """
    prompt = PromptTemplate.from_template(template)
    # llm=VertexAI()
    chain = prompt | llm
    answer = chain.invoke({"query": query})
    return f'{answer}'

def Fetch_from_api(query):
    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    search_url = f'{base_url}esearch.fcgi?db=pubmed&term={query}&retmode=json'
    response = requests.get(search_url)
    if response.status_code == 200:
        data = response.json()
        idlist = data['esearchresult']['idlist']
        content_url = []
        for id in idlist:
            content_url.append(f"https://pubmed.ncbi.nlm.nih.gov/{id}")
        
        template = """I am sending you a list of URL's {content_url}, go to each URL and get the best related data based on query{query}
    
        Answer: I want full abstarct of articles in text format"""
        prompt = PromptTemplate.from_template(template)
        chain = prompt | llm
        answer = chain.invoke({"content_url":content_url,"query": query})

    return f'{answer}'



@app.route('/')
def searchQueryForNewProject():
    return render_template('Main_page.html')

@app.route('/query', methods=['POST'])
def processQuery():
    try:
        data = request.get_json()
        query = data['query']  
        response = simulate_llm_model(query)
        if (response == " False"):
            response = Fetch_from_api(query)
            print("Response came from NCBI API")
        else:
            print("Response came from LLM")
        return jsonify({'result':response})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__=='__main__':
    app.run()
