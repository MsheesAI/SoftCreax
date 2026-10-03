import pathlib
import subprocess
from typing import Tuple

from langchain_core.tools import tool

PROJECT_ROOT = pathlib.Path.cwd() / "generated_project"

def safe_path_for_project(path:str) ->pathlib.Path:
    p = (PROJECT_ROOT/path).resolve()
    if PROJECT_ROOT.resolve() not in p.parents and PROJECT_ROOT.resolve() != p.parent and PROJECT_ROOT.resolve() != p:
        raise ValueError('Attempt to write outside the project')
    return p

@tool
def write_file(path:str,content:str)->str:
    """Writes content to a file at the specified path within the project root"""
    p = safe_path_for_project(path)
    p.parent.mkdir(parents=True,exist_ok=True)
    with open(p,'w',encoding="utf-8") as f:
        f.write(content)
    return f'WROTE:{p}'

@tool
def read_file(path:str)->str:
    """Reads content from a file at the specified path within the project root"""
    p = safe_path_for_project(path)
    if not p.exists():
        return " "
    with open(p,'r',encoding='utf-8') as f:
        return f.read()

@tool
def get_current_DIRECTORY()->str:
    """Returns the current working directory"""
    return str(PROJECT_ROOT)

@tool
def list_files(directory:str=".") -> str:
    """List all the files in the specified directory within the project root"""
    p = safe_path_for_project(directory)
    if not p.is_dir():
        return f"ERROR:{p} is not a directory"
    files = [str(f.relative_to(PROJECT_ROOT)) for f in p.glob("**/*") if f.is_file()]
    return "\n".join(files) if files else 'No files found.'


