from langchain.llms import VertexAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain,SimpleSequentialChain
import streamlit as st

llm = VertexAI(temperature=0)




def start(topic):

    get_title_name = PromptTemplate(
    input_variables =['topic'], 
    template = "Suggest Best Title for this topic {topic}"
)
    get_essay = PromptTemplate(
    input_variables =['essay'], 
    template = "write an essay for the title {essay}"
) 
    
    title = LLMChain(llm=llm, prompt=get_title_name)
    essay = LLMChain(llm=llm, prompt=get_essay)
    chain = SimpleSequentialChain(chains=[title,essay])
    content = chain.run(topic)
    
    return content

# print(start("Generative AI"))






