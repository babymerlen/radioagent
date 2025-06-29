from .graph import build_app
from langchain_core.messages import HumanMessage

app = build_app()


def run_program():
    print("=== Радио-агент ===")
    while True:
        query = input("Введите радиостанцию (или 'exit'): ").strip()
        if query.lower() in {"exit", "выход"}:
            break

        state = {"messages": [HumanMessage(content=query)]}
        result = app.invoke(state)
        print(result["messages"][-1].content)
        print("===")


if __name__ == "__main__":
    run_program()

#  python -m radio_agent.run
