from pydantic import BaseModel, Field , ConfigDict 
from typing import Optional


class File(BaseModel):
    path : str = Field(description="The path of the file to be created or modified ")
    purpose : str = Field(description="The purpose of the file to be created e.g 'main application logic , 'data processing module'")

class Plan(BaseModel):
    name : str = Field(description="The name of the Application to be built")
    description : str = Field(description="A brief description of the application e.g 'A web application for managing persons data'")
    tech_stack : str = Field(description="The tech stack to be used for the application e.g 'React, flask, Javascript , Python etc'")
    features:list[str] = Field(description="A list of features A app should have e.g 'User authentication, CRUD operations, Data visualization etc'")
    files : list[File] = Field(description="A list of files to be created each with a 'path'and 'purpose'")

class ImplementationTask(BaseModel):
    filepath:str = Field(description="The path to the file to be modified")
    task_description:str = Field(description="A detailed description of the task performed on the file")
class TaskPlan(BaseModel):
    implementation_steps:list[ImplementationTask] = Field(description="A list of steps to be taken to implement the task ")
    model_config = ConfigDict(extra="allow")

class CoderState(BaseModel):
    task_plan:TaskPlan = Field(description="The plan for the task to be implemented")
    current_step_index:int = Field(description="the index of the current step in the implementation steps")
    current_file_context:Optional[str] = Field(None,description="the context of the file currently being edited or created")