from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import time
"""
soup =  
coins = {coin's id : coin's name}
"""
# Create template of things I want to store:

market_cap = []
volume = []
timestamp = []
name = []
symbol = []
slug = []

# request main page to Bsoup object
cmc = requests.get("https://coinmarketcap.com/")
soup = BeautifulSoup(cmc.content, "html.parser")
# Prettify() of Bs4 enable us to view
# how the tags are nested
# print(soup.prettify())

# isolate JSON data within a script tag
# --------------------
data = soup.find("script", id="__NEXT_DATA__", type="application/json")
coins = {}
# using data.contents[0] to remove script tags
coin_data = json.loads(data.contents[0])
listings = coin_data["props"]["initialState"]["cryptocurrency"]["listingLatest"]["data"]

for i in listings:
    coins[str(i["id"])] = i["slug"]
# ---------------------

# get history price of every coins in coins{} list
# from  2020-01-01 to 2020-06-30
for i in coins:
    page = requests.get(f"https://coinmarketcap.com/currencies/{coins[i]}historical-data/?start=20200101&end=20200630")
    soup = BeautifulSoup(page.content, "html.parser")
    data = soup.find("script", id="__NEXT_DATA__", type="application/json")
    historical_data = json.loads(data.contents[0])
    # I want to understand the volume and market cap each day.
    # I find them nested accordingly:

    quotes = historical_data["props"]["initialState"]["cryptocurrency"]["ohlcvHistorical"][i]["quotes"]
    # I also want to log the info:
    info = historical_data['props']['initialState']['cryptocurrency']['ohlcvHistorical'][i]
#  sending data from beautifulsoup to arrays
#  and then into pandas data frame.
    for j in quotes:
        market_cap.append(j["quote"]["USD"]["market_cap"])
        volume.append(j["quote"]["USD"]["volume"])
        timestamp.append(j["quote"]["USD"]["timestamp"])
        name.append(info["name"])
        symbol.append(info["symbol"])
        slug.append(info[coins[i]])

df = pd.DataFrame(columns = ["marketcap", "volume", "timestamp", "name", "symbol", "slug"])
df["marketcap"] = market_cap
df["volume"] = volume
df["timestamp"] = timestamp
df["name"] = name
df["symbol"] = symbol
df["slug"] = slug
df.to_csv("criptoes.csv", index=False)

