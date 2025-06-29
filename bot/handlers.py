from aiogram import types, Router, F
from langchain_core.messages import HumanMessage
from radio_agent.graph import build_app, radiostation_db
from aiogram.filters import Command


app = build_app()
router = Router()


@router.message(F.text)
async def handle_radio_request(message: types.Message):
    user_input = message.text.strip()
    state = {"messages": [HumanMessage(content=user_input)]}
    final = app.invoke(state)
    last = final["messages"][-1]
    await message.answer(last.content)


@router.message(Command("stations"))
async def show_stations(message: types.Message):
    stations = list(radiostation_db.keys())
    text = "🎵 Доступные радиостанции:\n\n"
    text += "\n".join(f"• {name.title()}" for name in stations)
    await message.answer(text)
