#! /opt/homebrew/bin/python3

import requests
from pygrok import Grok
from bs4 import BeautifulSoup
import re

headers = { 'cache-control': 'no-cache',
'pragma': 'no-cache',
'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': '"macOS"',
'sec-fetch-dest': 'document',
'sec-fetch-mode': 'navigate',
'sec-fetch-site': 'none',
'sec-fetch-user': '?1',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

url = 'https://www.vesselfinder.com/vessels?type=604'
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'lxml')
#print (soup)
quotes = soup.find_all(class_='ship-link', href=True)
quotes2 = soup.find_all("span")

#print (quotes)
quotes2ext = quotes2[1].text.split(" / ")
print (quotes2ext[1])

for i in range(0, len(quotes)):
    href_p=quotes[i].get('href')
    print ("https://www.vesselfinder.com"+href_p)
