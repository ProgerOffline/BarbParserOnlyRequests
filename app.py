#-*- coding: utf-8 -*-

import asyncio
import aiohttp
import json
import random
import csv

from bs4 import BeautifulSoup
from masters_ids import MASTERS_IDS
from progress.bar import ShadyBar


phone_headers = {
    'Host': 'barb.pro',
    'Content-Length': '9',
    'Sec-Ch-Ua': '"(Not(A:Brand";v="8", "Chromium";v="98"',
    'X-Locale': 'ru',
    'X-Csrf-Token': 'bDAYrv6f1RRLt5IIPtNAE5C0IaB18w9OAZ3f6pHD',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'Sec-Ch-Ua-Platform': '"Linux"',
    'Origin': 'https://barb.pro',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://barb.pro/ru-ru/msk/master',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'close',
}

token_headers = {
    'Host': 'barb.pro',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Sec-Ch-Ua': '"(Not(A:Brand";v="8", "Chromium";v="98"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Linux"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'close',
}

proxies = [
    "http://89.191.225.117:59100", 
    "http://89.191.230.165:59100", 
    "http://185.29.124.225:59100", 
    "http://193.233.78.14:59100", 
    "http://45.89.188.97:59100", 
    "http://185.180.108.114:59100", 
    "http://45.128.184.18:59100", 
    "http://193.233.75.119:59100", 
    "http://193.233.75.97:59100", 
    "http://45.89.188.143:59100",
]


async def get_phone(session, proxy_auth, proxy, token, master_id):
    phone_headers['X-Csrf-Token'] = token 
    data = f'uid={master_id}'
    response = await session.post(
        url="https://barb.pro/ru-ru/ajax/getMePhones",
        data=data,
        headers=phone_headers,
        proxy=proxy,
        proxy_auth=proxy_auth,
        ssl=False,
    )
    
    if response.status == 200:
        response_data = json.loads(await response.text())
        soup = BeautifulSoup(response_data['phones'], "html.parser")
        phone = soup.a.text

    else:
        phone = None

    return phone


async def get_phones(token, ids):
    async with aiohttp.ClientSession() as session:
        proxy = random.choice(seq=proxies)
        proxy_auth = aiohttp.BasicAuth(
            login="progeroffline", 
            password="cQyjUk9FJd",
        )

        coros = (
            get_phone(
                session=session, 
                proxy_auth=proxy_auth, 
                proxy=proxy, 
                token=token,
                master_id=i,
            )
            
            for i in ids
        )

        phones = await asyncio.gather(*coros)

    return phones


async def get_token():
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            url="https://barb.pro/ru-ru/msk/master",
            headers=token_headers,
            ssl=False,
        )

        response_headers = response.raw_headers;
        for header in response_headers:
            key = header[0].decode(encoding="utf-8")
            value = header[1].decode(encoding="utf-8").split(sep=";")[0]

            if key.lower() == "set-cookie" and "laravel_session=" in value.lower():
                token = value.replace("laravel_session=", "")

    return token


async def main():
    table = open("Москва.csv", "w")
    writer = csv.writer(table)
    bar = ShadyBar("Parsing phones in Moscow", max=len(MASTERS_IDS))

    for i in range(3):
        token = await get_token()

        ids = MASTERS_IDS[i:i+10]
        phones = await get_phones(token, ids)
        
        [ writer.writerow([phone]) for phone in phones ]
        [ bar.next() for i in range(len(phones)) ]

    table.close()


if __name__ == "__main__":
    asyncio.run(main())