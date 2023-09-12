from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import VertexAI
from config import OPENAI_API_KEY,SERPAPI_API_KEY


import os
#os.environ['OPENAI_API_KEY']=OPENAI_API_KEY
os.environ['SERPAPI_API_KEY']=SERPAPI_API_KEY

def get_response(query):
    llm = VertexAI(temperature=0)

    #llm = OpenAI(temperature=0)
    tools = load_tools(["serpapi","llm-math"], llm=llm)
    agent = initialize_agent(tools,llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)


    # a = agent.run("How many Teslas have been sold in 2022. Multiple by 2")
    a = agent.run(query)
    print(f"Answer {a}")
    return a



# from langchain.output_parsers import CommaSeparatedListOutputParser
# from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate


# output_parser = CommaSeparatedListOutputParser()

# format_instructions = output_parser.get_format_instructions()
# prompt = PromptTemplate(
#     template="{subject}.\n{format_instructions}",
#     input_variables=["subject"],
#     partial_variables={"format_instructions": format_instructions}
# )

# model = VertexAI()

# _input = prompt.format(subject="How many Teslas have been sold in 2022. Multiple by 2")
# output = model(_input)

# print(output_parser.parse(output))
