import asyncio
from timeit import default_timer
from typing import final
from aiohttp import ClientSession
import time
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import csv

rows = []

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

headersCustom = headers

count = 2992

def getAddress(soup):
    try:
        address_container = soup.find(id="home-details-content")
        h1s = address_container.find_all("h1")

        for result in h1s:
            temp = result.text
            break

        temp_array = temp.split(",") 
        
        street_address = temp_array[0] 
        city = temp_array[1][1:]

        state_zip_split = temp_array[2].split(" ")
        state = state_zip_split[1]
        zipCode = state_zip_split[2]
        
        dictionary_for_url["street_address"]=str(street_address)
        dictionary_for_url["city"]=str(city)
        dictionary_for_url["state"]=str(state)
        dictionary_for_url["zip"]=str(zipCode)
    except:
        pass

def getPrice(soup):
    try:
        check = soup.find('span', class_='Text-c11n-8-37-1__aiai24-0 sXEJR')
        dictionary_for_url["price"] = str(check.text)
    except:
        try:
            check = soup.find('span', class_='Text-c11n-8-37-1__aiai24-0 sc-oTpqt jVKtyn') 
            deeper2 = check.find("span")
            deeper3 = deeper2.find("span")
            dictionary_for_url['price'] = str(deeper3.text)
        except:
            dictionary_for_url['price'] = 'None'
    
def getZestimate(soup):
    zestimate_container = soup.find(id='ds-home-values')
    try:
        deeper = zestimate_container.find("span", class_="Text-c11n-8-37-1__aiai24-0 kgcZzY")
        dictionary_for_url["zestimate"]=str(deeper.text)
    except:
        try:
            deeper = zestimate_container.find("span", class_="Text-c11n-8-37-1__aiai24-0 esBkDr")
            dictionary_for_url["zestimate"]=str(deeper.text)
        except:
            try:
                deeper = zestimate_container.find("h3", class_="Text-c11n-8-37-1__aiai24-0 StyledHeading-c11n-8-37-1__ktujwe-0 gpOnjE")
            except:
                dictionary_for_url["zestimate"]='None'

def getFacts(soup):
    facts_container = soup.find('div', class_='ds-home-facts-and-features reso-facts-features sheety-facts-features')
    try:
        sub = facts_container.find_all('span', class_='Text-c11n-8-37-1__aiai24-0 llYsPb')
        for elem in sub:
            attribute = elem.text
            array = attribute.split(":")
            dictionary_for_url[str(array[0])] = str(array[1])
    except:
        # try:
        #     sub = facts_container.find_all('span', class_='Text-c11n-8-37-1__aiai24-0 llYsPb')
        #     for elem in sub:
        #         attribute = elem.text
        #         array = attribute.split(":")
        #         dictionary_for_url[array[0]] = array[1]
        # except:
            print(facts_container)
            pass

def getRentZestimate(soup):
    try:
        rentZ = soup.find(id='ds-rental-home-values')
        rentZ_text = rentZ.find('span', class_='Text-c11n-8-37-1__aiai24-0 esBkDr')
        dictionary_for_url['Rent_Zestimate'] = str(rentZ_text.text)
    except:
        dictionary_for_url['Rent_Zestimate'] = 'None'


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
    wait = np.random.uniform(.5, 1)
    time.sleep(wait)
    global count
    global headersCustom
    if count % 50 == 0:
        wait = np.random.uniform(10, 20)
        headersCustom = headers2
    if count % 100 == 0:
        wait = np.random.uniform(20, 50)
        print('Waiting', wait, 'Seconds')
        time.sleep(wait)
        headersCustom = headers
    async with session.get(url, headers = headersCustom) as response:
        r = await response.read()
        soup = BeautifulSoup(r, "html.parser")
        
        global dictionary_for_url 
        dictionary_for_url = {}
        print(url)
        dictionary_for_url['url'] = url
        getAddress(soup)
        getPrice(soup)
        getZestimate(soup)
        getFacts(soup)
        getRentZestimate(soup)
        
        rows.append(dictionary_for_url)
     
        count += 1
        print(count)

# GET LINKS
filename = 'links.csv'
links = []
with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        links.append(row[1])
links.pop(0)

trigger = True
while (trigger):
    try:
        fetch_async(links[count:len(links)])
        trigger = False
    except:
        continue

final_df = pd.DataFrame(rows)

# comment out these two rows if first run starting
open_df = pd.read_csv('data.csv', index_col=0)
final_df = open_df.append(final_df, ignore_index=True)


final_df.to_csv('data.csv', header=True)

