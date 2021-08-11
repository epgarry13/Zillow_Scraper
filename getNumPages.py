import asyncio
from timeit import default_timer
from aiohttp import ClientSession
import time
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd


dictionary_of_urls = []

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
    wait = np.random.uniform(1, 1.5)
    time.sleep(wait)
    async with session.get(url, headers = headers2) as response:
        r = await response.read()
        soup = BeautifulSoup(r, "html.parser")
        agent_listings = soup.find_all("div", class_="total-text")  
        

        try:
            for num in agent_listings:
                number = num.text                
                numPages = round(int(number.replace(",",""))/40)
                break
        except:
            numPages = 20
            
        temp_dict = {}
        temp_dict['url'] = url
        temp_dict['NumPages'] = numPages
        dictionary_of_urls.append(temp_dict)

        global count
        count += 1
        print(count)



# links = []

count = 0
startZip = 77001
maxZip = 77598

starting_links = []
for i in range (startZip, maxZip + 1):
    baseZipURL = "https://www.zillow.com/houston-tx-" + f'{i}' + "/"
    starting_links.append(baseZipURL)

# print(starting_links)
fetch_async(starting_links)

numPagesCSV = pd.DataFrame(dictionary_of_urls)
numPagesCSV.to_csv('numPages.csv')