from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from prompts import prompt
from states import *
from langgraph.constants import END
from langgraph.graph import StateGraph
from tools import read_file, write_file , list_files , get_current_DIRECTORY
from langchain.agents import create_agent

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model='openai/gpt-oss-120b', groq_api_key=api_key)

user_prompt = "Create a simple calculator web application"

def planner_agent(state:dict) -> dict:
    user_prompt = state['user_prompt']
    resp = llm.with_structured_output(Plan,method='json_schema').invoke(prompt.Planner_prompt(user_prompt))
    return {'plan': resp}

def architect_agent(state:dict) -> dict:
     plan:Plan = state['plan'] 
     resp = llm.with_structured_output(TaskPlan,method='json_schema').invoke(prompt.architect_prompt(plan))
     if resp is None:
          raise ValueError("Architect didnt return valid response")
     
     return {'task_plan': resp}

def coder_agent(state:dict) -> dict:
     steps = state['task_plan'].implementation_steps
     current_step_index = 0
     current_task = steps[current_step_index]
     existing_content = read_file.run(current_task.filepath)

     user_prompt = (
          f"Task: {current_task.task_description}\n"
          f"File:{current_task.filepath}\n"
          f"Existing content:\n{existing_content}\n"
     )
     system_prompt= prompt.coder_system_prompt()
     coder_tools = [read_file,write_file,list_files,get_current_DIRECTORY]
     react_agent = create_agent(llm,coder_tools)   
     react_agent.invoke({'messages':[{'role':'system','content':system_prompt},{'role':'user','content':user_prompt}]})
     return {}



graph = StateGraph(dict)
graph.add_node('planner',planner_agent)
graph.add_node('architect',architect_agent)
graph.add_node('coder',coder_agent)

graph.add_edge('planner', 'architect')
graph.add_edge('architect', 'coder')

graph.set_entry_point('planner')

agent = graph.compile()

user_prompt = 'Create a simple Calculator Web Application'

result = agent.invoke({'user_prompt': user_prompt})
print(result)
