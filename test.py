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
    
# for game in top_game_list: we can extract useful information including
# categories, description, mechanics, min/maxplayers, playingtime, minage, averageWeight
g = bgg.game(name="Through the Ages: A New Story of Civilization", comments=True)
with open("Through the Ages: A New Story of Civilization.txt", "w") as f:
    for i in range(len(g.comments)):
        if len(g.comments[i]._data['comment']) > 50:
            f.write(g.comments[i]._data['comment'])
            f.write("\n")

from langchain.embeddings import HuggingFaceBgeEmbeddings

model_name = "BAAI/bge-large-en-v1.5"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
hf = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

# embedding = hf.embed_query("How are you doing today?")
# embedding[0]

# pgvector
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.pgvector import PGVector
from langchain.document_loaders import TextLoader

loader = TextLoader("Through the Ages: A New Story of Civilization.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

CONNECTION_STRING = "postgresql+psycopg2://kenzgf:@localhost:5432/postgres"

COLLECTION_NAME = "tta_test"

db = PGVector.from_documents(
    embedding=hf,
    documents=docs,
    collection_name=COLLECTION_NAME,
    connection_string=CONNECTION_STRING,
)
