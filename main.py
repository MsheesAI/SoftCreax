from agent.graph import agent

user_prompt = "Create a simple Calculator Web Application"

result = agent.invoke(
    {"user_prompt": user_prompt},
    {"recursion_limit": 100}
)

print(result)