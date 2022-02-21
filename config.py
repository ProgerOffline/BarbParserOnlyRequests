#-*- coding: utf-8 -*-

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
    "http://185.180.108.23:59100",
    "http://185.180.108.154:59100",
    "http://185.180.109.9:59100",
    "http://193.42.108.187:59100",
    "http://193.42.108.168:59100",
    "http://193.42.108.143:59100",
]

count_attempts = {}