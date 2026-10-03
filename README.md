# SoftCreax

SoftCreax is an AI app builder. You describe an application in plain English, and a team of LLM agents plans it, designs the file-by-file implementation, and writes the code to disk.

> **Status:** early prototype (v0.1). The planning pipeline works end to end; the coding stage is still being built out (see [Current limitations](#current-limitations)).

## How it works

SoftCreax is a [LangGraph](https://langchain-ai.github.io/langgraph/) pipeline of three agents, powered by `openai/gpt-oss-120b` served through [Groq](https://groq.com/):

```
user prompt ──▶ Planner ──▶ Architect ──▶ Coder ──▶ generated_project/
```

| Agent | What it does | Output |
|-------|--------------|--------|
| **Planner** | Turns the prompt into a project plan: app name, description, tech stack, features, and the list of files with their purpose. | `Plan` |
| **Architect** | Converts the plan into ordered implementation tasks, one or more per file, with enough detail that the coder doesn't have to make architectural decisions. | `TaskPlan` |
| **Coder** | A tool-using agent that reads existing files and writes the full file content. | Files in `generated_project/` |

The planner and architect use structured output (JSON schema, validated by Pydantic), so their results are typed objects rather than free text.

### Coder tools

The coder agent can call four tools, all sandboxed to the `generated_project/` folder (writes outside it are rejected):

- `write_file(path, content)`: create or overwrite a file
- `read_file(path)`: read a file (returns blank if it doesn't exist)
- `list_files(directory)`: list files under a directory
- `get_current_DIRECTORY()`: return the project root path

## Project structure

```
softcreax/
├── main.py                 # Placeholder entry point
├── pyproject.toml          # Dependencies and Python version
├── uv.lock
└── agent/
    ├── graph.py            # LangGraph pipeline (planner → architect → coder) and run script
    ├── states.py           # Pydantic models: Plan, File, TaskPlan, ImplementationTask
    ├── tools.py            # Sandboxed file tools for the coder agent
    ├── prompts/
    │   └── prompt.py       # Planner, architect, and coder prompts
    └── generated_project/  # Where generated apps are written
```

## Getting started

### Prerequisites

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- A [Groq API key](https://console.groq.com/keys)

### Installation

```bash
git clone https://github.com/MsheesAI/SoftCreax.git
cd SoftCreax
uv sync
```

### Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Run

The agent imports its sibling modules directly, so run it from inside the `agent/` folder. Generated files are written to `agent/generated_project/`.

```bash
cd agent
uv run graph.py
```

The prompt is currently set in `agent/graph.py` (`user_prompt`). By default it is:

```python
user_prompt = 'Create a simple Calculator Web Application'
```

Edit that line to build something else.

## Tech stack

- [LangGraph](https://langchain-ai.github.io/langgraph/) for agent orchestration
- [LangChain](https://www.langchain.com/) (`langchain`, `langchain-core`, `langchain-groq`) for agents and tools
- [Groq](https://groq.com/) for LLM inference
- [Pydantic](https://docs.pydantic.dev/) for structured output schemas
- [python-dotenv](https://github.com/theskumar/python-dotenv) for configuration

## Current limitations

- **The coder only handles the first task.** It currently implements just the first step of the architect's plan instead of looping through every file, so most generated projects will be incomplete. (The sample in `agent/generated_project/` contains only an `index.html` for the calculator.)
- **The prompt is hard-coded** in `agent/graph.py`; there is no CLI or UI yet.
- **`main.py` is a stub** and doesn't launch the pipeline.

## Roadmap

- [ ] Loop the coder over all implementation steps
- [ ] Accept the prompt from the command line (and wire up `main.py`)
- [ ] Web UI for entering prompts and previewing generated apps
- [ ] Support more models and providers

## Contributing

Issues and pull requests are welcome. For larger changes, please open an issue first to discuss what you'd like to change.

## License

No license has been specified yet
