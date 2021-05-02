import requests
import pandas as pd
import os
from github import Github

from datetime import datetime
from pytz import timezone

tz = timezone('US/Eastern')
date = lambda: str(datetime.now(tz).date())

CMC = os.getenv('CMC')
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

parameters = {
    'limit': 5000,
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': CMC,
    'Accept-Encoding': 'deflate, gzip'
}
resp = requests.get(
    url,
    headers=headers,
    params=parameters
).json()
print(resp)

names = [
    x['name']
    for x in resp['data']
]
quotes = [
    x['quote']['USD']
    for x in resp['data']
]

df = pd.DataFrame(quotes)
df.insert(0, 'name', names)
data = df.to_csv()

GITHUB = os.getenv('GITHUB')
g = Github(GITHUB)

repo = g.get_repo("GeorgeFane/cmc-api")
repo.create_file('data/' + date(), date(), data)
