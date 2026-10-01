from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from prompts import prompt

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model='openai/gpt-oss-120b', groq_api_key=api_key)

user_prompt = "Create a simple calculator web application"

prompt = prompt.Planner_prompt(user_prompt)

class File(BaseModel):
    path : str = Field(description="The path of the file to be created or modified ")
    purpose : str = Field(description="The purpose of the file to be created e.g 'main application logic , 'data processing module'")

class Plan(BaseModel):
    name : str = Field(description="The name of the Application to be built")
    description : str = Field(description="A brief description of the application e.g 'A web application for managing persons data'")
    tech_stack : str = Field(description="The tech stack to be used for the application e.g 'React, flask, Javascript , Python etc'")
    features:list[str] = Field(description="A list of features A app should have e.g 'User authentication, CRUD operations, Data visualization etc'")
    files : list[File] = Field(description="A list of files to be created each with a 'path'and 'purpose'")




resp = llm.with_structured_output(Plan,method='json_schema').invoke(prompt)
print(resp)
