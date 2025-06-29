from langchain_openai import ChatOpenAI
from .tools import tools

model = ChatOpenAI(
    model="google/gemini-flash-1.5",
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.5
).bind_tools(tools)
