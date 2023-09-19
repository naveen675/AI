import streamlit as st
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
# import google.auth
# from htmlTemplates import css, bot_template, user_template


embedding_model_name = os.environ.get('EMBEDDING_MODEL_NAME')

def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text+=page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=20, length_function=len)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings=HuggingFaceEmbeddings()
    #embeddings=HuggingFaceEmbeddings(model_name = embedding_model_name)
    vectorstore = FAISS.from_texts(text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = VertexAI(model_name="text-bison@001",
        max_output_tokens=256,
        temperature=0.1,
        top_p=0.8,
        top_k=40,
        verbose=True,
       
        )
    #llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm,retriever=vectorstore.as_retriever(),memory=memory)
    return conversation_chain

def handle_user_input(user_question):

    sys = f'''
    You are a Q and A So you need to answer only for the questions that are related to the ducuments
    that you are trained on. If the information is not in document then Mention as
    "I am sorry, This Information is not available in the provided Documents."
    Please answer to below query
    
    '''
    prompt = f"{sys} \n {user_question}"
    print(prompt)

    #     Example : 
    # Input 
    # Who will be last person On earth
    # Output 
    # I am sorry, This Information is not available in the provided Documents.
    # -------------------------------
    # Input 
    prompt = f"{sys} \n {user_question}"
    print(prompt)
    
    response=st.session_state.conversation({'question':prompt})
    #st.write(response)
    st.session_state.chat_history = response['chat_history']
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2==0:
            st.write("**Humar Query**")
            st.write(user_question)
            st.write("**AI Prompt**")
            st.write(message.content)
        else:
            #st.write(message)
            st.write("**AI Response**")
            st.write(message.content)



def main():
    load_dotenv()
    # credentials, project = google.auth.default()
    st.set_page_config("Chat with Multiple PDF's")
    #st.write(css, unsafe_allow_html=True)
    st.markdown("Pull left side bar on top to upload documents")
    st.header("Chat with Multiple PDFs")
    st.write("**Things to do before firing queries**")
    st.markdown("- Upload your document (Only Pdf) and click on process")
    st.markdown("- Once Processing is done")
    st.markdown("- You can start chatting with your documents")
    if "conversation" not in st.session_state:
        st.session_state.conversation=None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history=None
    user_question = st.text_input("Ask a question from your documents after uploading your documents")
    if user_question:
        handle_user_input(user_question)
    with st.sidebar:
        st.header("Chat with PDF ")
        st.title("LLM Chatapp using LangChain")
        pdf_docs = st.file_uploader("Upload the PDF Files here and Click on Process", accept_multiple_files=True)
        
        
        if st.button('Process'):
            with st.spinner("Processing"):
                
                raw_text = get_pdf_text(pdf_docs)
                
                text_chunks = get_text_chunks(raw_text)
                
                vectorstore=get_vector_store(text_chunks)
                
                
                st.session_state.conversation=get_conversation_chain(vectorstore)
                st.success("Done!")

    # Github = "https://github.com/naveen675/AI/tree/main/langchain"


    # col1, col2 = st.columns([1, 3])


    # col1.image("github-512.webp", width=30)


    # col2.markdown(f"[ClickHere]({Github})", unsafe_allow_html=True)

        
    # linkedin_url = "https://www.linkedin.com/in/naveen675"


    # col1, col2 = st.columns([1, 3])


    # col1.image("circle-linkedin-512.webp", width=30)


    # col2.markdown(f"[ClickHere]({linkedin_url})", unsafe_allow_html=True)
        
        # Github_Code = "https://github.com/naveen675/AI/tree/main/langchain"


        # link_html = f'<a href="{Github_Code}" target="_blank"><img src="github-512.webp" width="40"></a>'
        # st.markdown(link_html, unsafe_allow_html=True)

        # linkedin_url = "https://www.linkedin.com/in/naveen675"


        # link_html = f'<a href="{linkedin_url}" target="_blank"><img src="circle-linkedin-512.webp" width="40"></a>'
        # st.markdown(link_html, unsafe_allow_html=True)
        # # st.markdown(f'<a href="{linkedin_url}" target="_blank"><img src="circle-linkedin-512.webp" width="30"></a>', unsafe_allow_html=True)
        # st.write(f"[![LinkedIn](circle-linkedin-512.webp)]({linkedin_url})", unsafe_allow_html=True)


    

if __name__ == "__main__":
    main()

    Github = "https://github.com/naveen675/AI/tree/main/langchain"


    col1, col2 = st.columns([1, 3])


    col1.image("github-512.webp", width=30)


    col2.markdown(f"[ClickHere]({Github})", unsafe_allow_html=True)

        
    linkedin_url = "https://www.linkedin.com/in/naveen675"


    col1, col2 = st.columns([1, 3])


    col1.image("circle-linkedin-512.webp", width=30)


    col2.markdown(f"[ClickHere]({linkedin_url})", unsafe_allow_html=True)