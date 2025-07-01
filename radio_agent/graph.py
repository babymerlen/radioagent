from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage, AIMessage, ToolMessage

from .state import AgentState
from .tools import tools
from .stations import radiostation_db
from .model import model


def song_agent(state: AgentState) -> AgentState:
    messages = list(state["messages"])
    if isinstance(messages[-1], ToolMessage):
        result = messages[-1].content
        return {"messages": messages + [AIMessage(content=f"♪ Сейчас играет: {result}")]}

    system_prompt = SystemMessage(
        content=(
            "Ты — ИИ-агент, который может определять название радиостанции по запросу пользователя "
            "и использовать инструмент get_song, чтобы получить текущую песню на этой станции.\n"
            f"У тебя есть список радиостанций:\n{list(radiostation_db.keys())}\n"
            f"Какой из них наиболее подходит под запрос пользователя? "
            f"Выбери вариант наиболее подходящий под запрос"
            "После этого ВЫЗОВИ инструмент get_song с этим названием. "
            "НЕ просто возвращай название станции как текст. "
            "Если не удалось понять, что за станция — скажи пользователю, что не получилось распознать"
            " и предложи варианты из наиболее похожих или воспользоваться командой /stations"
        )
    )
    full_messages = [system_prompt] + messages
    result = model.invoke(full_messages)
    return {"messages": messages + [result]}


def should_continue(state: AgentState) -> str:
    messages = state["messages"]
    if isinstance(messages[-1], ToolMessage):
        return "continue"
    if isinstance(messages[-1], AIMessage):
        return "end"
    return "continue"


def build_app():
    graph = StateGraph(AgentState)
    tool_node = ToolNode(tools=tools)
    graph.add_node("agent", song_agent)
    graph.add_node("tools", tool_node)
    graph.set_entry_point("agent")
    graph.add_edge("agent", "tools")
    graph.add_conditional_edges(
        "tools",
        should_continue,
        {
            "continue": "agent",
            "end": END
        }
    )
    return graph.compile()
