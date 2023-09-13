from PyPDF2 import PdfReader
from langchain.embeddings import VertexAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import VertexAI


def data():
    reader = PdfReader('Amazon Paper of Month.pdf')

    pdf_data = ''
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pdf_data += text

    # print(pdf_data)

    splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size=4000,
        chunk_overlap = 200,
        length_function=len

    )

    chunks = splitter.split_text(pdf_data)

    # print(len(chunks))

    embeded = VertexAIEmbeddings()
    embeded_doc = FAISS.from_texts(chunks, embeded)


    llm = VertexAI()
    chain = load_qa_chain(llm, chain_type = 'stuff')
    query = "Who are the authors of this article  Using Lightweight Formal Methods to Validate a Key-Value Storage Node in Amazon S3"
    docs = embeded_doc.similarity_search(query)
    text = chain.run(input_documents=docs, question=query)
    return text

#data()