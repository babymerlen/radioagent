from langchain_core.tools import tool
from .stations import radiostation_db
import requests


@tool
def get_song(radiostation: str) -> str:
    """Получает текущую песню по названию радиостанции"""
    radio_url = requests.get(radiostation_db[radiostation.lower()])
    if radio_url:
        data = radio_url.json()
        song_info = data.get("metadata", "")
        if "***" in song_info or not song_info:
            return "Песня только началась или временно недоступна, попробуйте позже."
        return song_info
    return "Не удалось получить данные с сервера."


tools = [get_song]