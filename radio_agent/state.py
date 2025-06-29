from typing import TypedDict, Annotated, Sequence, Union
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage


class AgentState(TypedDict):
    messages: Annotated[Sequence[Union[HumanMessage, AIMessage, ToolMessage]], add_messages]

