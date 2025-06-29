from dotenv import load_dotenv
import os
import requests
import json
USER_AGENT = os.getenv("USER_AGENT")
load_dotenv()
from bs4 import BeautifulSoup


def create_radiostations_db():
    url = "https://music.mts.ru/radio"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.find('script', {'id': '__NEXT_DATA__', 'type': 'application/json'})
    data_json = script_tag.string
    data = json.loads(data_json)
    stations = data['props']['pageProps']['radio']
    radio_db = {station['title'].lower(): station['metaData']['jsonUrl'][:-10]+"current.json"
                for station in stations if station['metaData']}
    return radio_db


radiostation_db = create_radiostations_db()
