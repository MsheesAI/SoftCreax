from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from prompts import prompt
from states import *
from langgraph.constants import END
from langgraph.graph import StateGraph

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model='openai/gpt-oss-120b', groq_api_key=api_key)

user_prompt = "Create a simple calculator web application"

def planner_agent(state:dict) -> dict:
    user_prompt = state['user_prompt']
    resp = llm.with_structured_output(Plan,method='json_schema').invoke(prompt.Planner_prompt(user_prompt))
    return {'plan': resp}

graph = StateGraph(dict)
graph.add_node('planner',planner_agent)
graph.set_entry_point('planner')

agent = graph.compile()

user_prompt = 'Create a simple Calculator Web Application'

result = agent.invoke({'user_prompt': user_prompt})
print(result)
