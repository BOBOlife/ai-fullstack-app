import os

from dotenv import load_dotenv
from fastapi import FastAPI
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()

app = FastAPI()

model = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/",
)


@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"


@tool
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    return f"Weather in {location}: Sunny, 24°C"


agent = create_agent(
    model,
    tools=[search, get_weather],
    system_prompt="You are a helpful assistant",
)
question = input("请输入你的问题：")
# Run the agent
result = agent.invoke({"messages": [{"role": "user", "content": question}]})

print(result["messages"][-1].content)
