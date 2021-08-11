import asyncio
from timeit import default_timer
from aiohttp import ClientSession
import time
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import csv

headers = {
     'authority': 'www.zillow.com',
     'method': 'GET',
     'scheme': 'https',
     'accept': 'application/json, text/plain, */*',
     'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36'
}

headers2 = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'sec-ch-ua-mobile': '?1',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36'
}


def fetch_async(urls):
    start_time= default_timer()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(fetcheverything(urls))
    loop.run_until_complete(future)
    
    time_taken = default_timer()-start_time
    print('Time taken:', time_taken)

async def fetcheverything(urls):
    tasks = []
    async with ClientSession() as session:
        for url in urls:
            task =asyncio.ensure_future(fetch(url, session))
            tasks.append(task)
            _= await asyncio.gather(*tasks)

async def fetch(url, session):
    wait = np.random.uniform(2, 5)
    time.sleep(wait)
    async with session.get(url, headers = headers2) as response:
        r = await response.read()

        print(url)
        html_on_page = str(r)
        split_html = html_on_page.split('\"')
        count_num_links = 0
        for n in range(0, len(split_html)):
            if "https://www.zillow.com/homedetails" in split_html[n]:
                if split_html[n] not in links:
                    links.append(split_html[n])
                    count_num_links += 1
        

        global count
        count += 1
        print('Completed: ',count)



links = []
count = 0

filename = 'numPages.csv'
numPages = {}
with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        numPages[row[1]] = row[2]

allLinksToLoopThrough = []

for key in numPages:

    if (key != 'url') and (key != '0') and (key != 0):
        allLinksToLoopThrough.append(key)
        for i in range (2, min(21, int(numPages[key]))):
            new_url = key + f'{i}' + "_p/"
            allLinksToLoopThrough.append(new_url)

# print(allLinksToLoopThrough)


fetch_async(allLinksToLoopThrough)

link_df = pd.DataFrame({'links': links})
link_df.to_csv('links.csv')
