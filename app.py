#-*- coding: utf-8 -*-

import asyncio
import aiohttp
import json
import random
import csv

from bs4 import BeautifulSoup
from masters_ids import MASTERS_IDS
from progress.bar import ShadyBar
from config import *


async def create_session():
    session = aiohttp.ClientSession()
    proxy_auth = aiohttp.BasicAuth(
        login="progeroffline", 
        password="cQyjUk9FJd",
    )
    proxy = random.choice(seq=proxies)
    

    return session, proxy_auth, proxy


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

        attempt = count_attempts.get(master_id)
        if attempt:
            count_attempts[master_id] += 1
            print(f"✅ {proxy} : {master_id} : {count_attempts[master_id]}")
        else:
            count_attempts[master_id] = 1
            print(f"✅ {proxy} : {master_id} : {count_attempts[master_id]}")

    else:
        attempt = count_attempts.get(master_id)
        if attempt:
            count_attempts[master_id] += 1
            print(f"❌ {proxy} : {master_id} : {count_attempts[master_id]}")
        else:
            count_attempts[master_id] = 1
            print(f"❌ {proxy} : {master_id} : {count_attempts[master_id]}")
        
        second_session, proxy_auth, proxy = await create_session()
        async with second_session:
            phone = await get_phone(
                session=second_session,
                proxy_auth=proxy_auth,
                proxy=proxy,
                token=await get_token(),
                master_id=master_id,
            )

    return phone


async def get_phones(token, ids):
    print(f"\nMasters IDS : {ids}")
    session, proxy_auth, proxy = await create_session()
    async with session:
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
            url="https://barb.pro/ru-ru/spb/master",
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
    offset = open("offset.txt")
    offset = int(offset.read())
    masters_ids = MASTERS_IDS[offset-1:]

    table = open("Москва.csv", "w")
    writer = csv.writer(table)
    bar = ShadyBar("Parsing phones in Moscow", max=len(masters_ids))

    for i in range(0, len(masters_ids), 10):
        token = await get_token()

        ids = masters_ids[i:i+10]
        phones = await get_phones(token, ids)
        
        [ writer.writerow([phone]) for phone in phones ]
        [ bar.next() for i in range(len(phones)) ]

    table.close()


if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            print(e)
            offset = open("offset.txt", "r")
            offset = int(offset.read())
            table = open("Москва.csv", "r")
            reader = csv.reader(table)
            phones = [ row for row in reader ]

            new_table = open(f"Москва{offset}_{len(phones)}.csv", "w")
            writer = csv.writer(new_table)

            [ writer.writerow(phone) for phone in phones ]

            table.close()
            new_table.close()

            with open("offset.txt", "w") as file:
                file.write(str(len(phones)))