#! /opt/homebrew/bin/python3

import requests
#import urllib
import os
import codecs
import gc
from datetime import date
from random import randint
from bs4 import BeautifulSoup

URLHOME = 'https://www.vesselfinder.com'
URLLNG = 'https://www.vesselfinder.com/vessels?type=604'
            
def parser(url):
    data = []
    proxyline = 0
    with open("proxy.list") as f:
        for line in f:
            data.append(line.split("\n"))
            proxyline=proxyline+1

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

    store = URLHOME.split('/')
    store = store[2].split('.')
    value = randint(0, proxyline -1)

    while(True):
        try:
            http_proxy = data[value][0]
            proxyDict = { "http" : http_proxy }
            print (http_proxy)
            r = requests.get(url, proxies=proxyDict, headers=headers)
            er=1
        except:
            print("Повтор запроса: "+url)
            er=0
        if (er == 1 and r.status_code == 200):
            break
    soup = BeautifulSoup(r.text, 'lxml')

    title = soup.find_all('h1', class_='title')

    rout = soup.find_all(class_='flx _rLk')

    portcalls = soup.find_all(class_='column ship-section')
    flx = soup.find_all(class_='flx')
    #print (flx[5])


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
    
    except:
        textprinttextfrom = "none"
        warningfrom = "no"
        textprinttextto = "none"
        warningfto = "no"
        flagtext = "none"
        deadweight = "0"

    jsondata = []

    jsondata.append("<LNG><name>"+namelng+"</name><from>"+textprinttextfrom+"</from><fromrussian>"+warningfrom+"</fromrussian><to>"+textprinttextto+"</to><torussian>"+warningfto+"</torussian><flag>"+flagtext+"</flag><deadweight>"+deadweight+"</deadweight></LNG>") 
    ###############
    today = date.today()
    d1 = today.strftime("%d-%m-%Y")
    mode = 0o744
    try:
        cwd = os.getcwd() 
        os.mkdir(cwd+"/output-xml-"+d1, mode)
    except OSError:
        #print("Папка уже создана!")
        n = gc.collect()

    textfile = codecs.open(cwd+"/output-xml-"+d1+"/lng-"+d1+".xml", "a", "utf-8")
    for element in jsondata:
        textfile.write(element + "\n")
    textfile.close()

def preparser(href_p):
        ##########
        pageint = 1
        data = []
        proxyline = 0
        with open("proxy.list") as f:
            for line in f:
                data.append(line.split("\n"))
                proxyline=proxyline+1
        urlin = (href_p)
        url = urlin
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

        print (url)
        value = randint(0, proxyline -1)

        while(True):
            url = URLLNG+"&page="+str(pageint)
            print (url)
            while(True):
                try:
                    http_proxy = data[value][0]
                    proxyDict = { "http" : http_proxy }
                    print (http_proxy)
                    r = requests.get(url, proxies=proxyDict, headers=headers)  
                    er=1
                except:
                    print("Повтор запроса: "+url)
                    er=0
                if (er == 1 and r.status_code == 200):
                    break 
            soup = BeautifulSoup(r.text, 'lxml')

            quotes = soup.find_all(class_='ship-link', href=True)
            quotes2 = soup.find_all("span")

            #print (quotes)
            quotes2ext = quotes2[1].text.split(" / ")
            pagetext = quotes2ext[1]

            for z in range(0, len(quotes)):
                href_p=quotes[z].get('href')
                print (URLHOME+href_p)
                parser(URLHOME+href_p)
            pageint = pageint + 1
            print (str(pageint)+" | "+str(pagetext))
            if (pageint == int(pagetext)):
                break

if __name__ == "__main__":
    url = URLHOME
    preparser(url)