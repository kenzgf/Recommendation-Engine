# from langchain.llms import OpenAI

# llm = OpenAI(openai_api_key="")

# text = "How are you doing today?"
# print(llm.predict(text))

import requests
import xml.dom.minidom

url = "https://boardgamegeek.com/xmlapi2/search"

res = requests.get(url, params={"query": "ark nova", "exact": 1})
tmp = xml.dom.minidom.parseString(res.text)
tmp = tmp.toprettyxml()
tmp = '\n'.join([line for line in tmp.splitlines() if line.strip()])
print(tmp)

# interested in: game name, description, minmax players, playtime, rating, 
# language dependance, weight, type

from boardgamegeek import BGGClient

bgg = BGGClient()
g = bgg.game("Through the Ages: A New Story of Civilization", comments=True)
comments = g.comments
comments[0]._data['comment']

g = bgg.hot_items("boardgame")

from urllib.request import urlopen
from bs4 import BeautifulSoup

top_game_list = [] # a list of top 1000 games. This is static for now. 
for i in range(1, 11):
    url = "https://boardgamegeek.com/browse/boardgame/page/" + str(i)
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
    for a_tag in soup.find_all('a', href=True, class_='primary'):
        if a_tag['href'].startswith("/boardgame/"):
            top_game_list.append(a_tag.text)

hot_game_list = [] # a list of hot games. This is periodically updated.
bgg = BGGClient()
g = bgg.hot_items("boardgame")
for game in g:
    hot_game_list.append(game.name)

