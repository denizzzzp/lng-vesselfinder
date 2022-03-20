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

url = "https://www.vesselfinder.com/vessels/SEISHU-MARU-IMO-9666558-MMSI-0"
urlcat = url.split('/')
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'lxml')
title = soup.find_all('h1', class_='title')

rout = soup.find_all(class_='flx _rLk')

flag = soup.find_all(class_='_npNa')
portcalls = soup.find_all(class_='column ship-section')
flx = soup.find_all(class_='flx')
#print (flx[5])

quotes = soup.find_all('div', class_='ProductsBox__listItem')
end = soup.find_all('a', class_='Pagination__directionLink', attrs={"aria-disabled" : re.compile(".*"), "aria-label" : "Next page"})

namelng = title[0].text

try:
    routeto = rout[0].text
    routefrom = rout[1].text

    routefromar = routefrom.splitlines()
    routetoar = routeto.splitlines()

    #print (rout[0].text)
    #print (rout[1].text)


    wdf=flx[5].text
    wd=portcalls[4].text

    wdfs=wdf.splitlines()
    wds=wd.splitlines()
    printtextfrom = ""
    printtextto = ""

    for z in range(0, len(routefromar)):
        if (routefromar[z] != ""):
            printtextfrom = printtextfrom +" "+routefromar[z]
    textprinttextfrom = printtextfrom.strip()
    if ("Russia" in textprinttextfrom):
        warningfrom = "yes"
    else:
        warningfrom = "no"

    for x in range(0, len(routetoar)):
        if (routetoar[x] != ""):
            printtextto = printtextto +" "+routetoar[x]
    textprinttextto = printtextto.strip()
    if ("Russia" in textprinttextto):
        warningfto = "yes"
    else:
        warningfto = "no"

    for u in range(0, len(wdfs)):
        if ("Flag" in wdfs[u]):
            textwdfs = wdfs[u].split("Flag")
            flagtext = (textwdfs[1])

    for i in range(0, len(wds)):
        if ("Deadweight" in wds[i]):
            textwds = wds[i].split("(t)")
            deadweight = (textwds[1])

    #print (namelng)
    #print (textprinttextfrom)
    #print (warningfrom)
    #print (textprinttextto)
    #print (warningfto)
    #print (flagtext)
    #print (deadweight)
except:
    textprinttextfrom = "none"
    warningfrom = "no"
    textprinttextto = "none"
    warningfto = "no"
    flagtext = "none"
    deadweight = "0"
print ("<LNG><name>"+namelng+"</name><from>"+textprinttextfrom+"</from><fromrussian>"+warningfrom+"</fromrussian><to>"+textprinttextto+"</to><torussian>"+warningfto+"</torussian><flag>"+flagtext+"</flag><deadweight>"+deadweight+"</deadweight></LNG>")


# for i in range(0, len(portcalls)):
#     text_p=portcalls[4].text
#     print (text_p)
#     if ("Deadweight" in text_p):
#         print (text_p)
