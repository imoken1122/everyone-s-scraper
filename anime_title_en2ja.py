
from selenium import webdriver
import time
from tqdm import tqdm
import chromedriver_binary
import pickle
from bs4 import BeautifulSoup
import argparse as ap
import os
import re
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    return driver


def get_title(driver,url,en_title,tag):
    driver.get(f"{url} {en_title}")
    print(f"{url} {en_title}")
    time.sleep(2)
    html = driver.page_source

    soup = BeautifulSoup(html, "lxml")
    title = soup.select(tag)
    print(title)
    return title

def scraper(driver,en_title):
    url = 'https://www.google.co.jp/search?num=1&q=アニメ'
    tag = "h2.qrShPb.kno-ecr-pt.PZPZlf.mfMhoc> span"
    title = get_title(driver,url,en_title,tag)
    if len(title) != 0:
        title = title[0].get_text()
        print(f"[1]  en:{en_title} || ja:{title}")
        return title
    
    else:

        url = 'https://www.google.co.jp/search?num=1&q=wikipedia'
        tag = "h3.LC20lb.DKV0Md"
        title = get_title(driver,url,en_title,tag)
        if len(title) == 0:
            return en_title 
        else:
            title = title[0].get_text()

        if title.find(' - ウィキペディア') >= 0:
            title = title.replace(' - ウィキペディア',"")
        if title.find(' - Wikipedia') >= 0:
            title = title.replace(' - Wikipedia',"")
        else:
            print('エラー:検索失敗 - ', en_title,title)
            return title
       
        # カッコの削除
        if title.find("("):
            title = title.split('(')[0]
        if title.find(" ("):
            title = title.split(' (')[0]        
        print(f"[2]  en:{en_title} || ja:{title}")
        return title




driver = get_driver()

with open("id2anime.pkl","rb") as f:
    id2anime = pickle.load(f)

def load_pkl():
    with open('en2ja.pkl','rb') as f:
        a = pickle.load(f)
    return a

def output(en2ja,name = "en2ja.pkl"):
    print("save pickle")
    with open(name, 'wb') as f:
        pickle.dump(en2ja, f) 

def first():
    en2ja = {}
    cnt = 0
    for k,v in tqdm(id2anime.items()):
        en2ja[v] = scraper(driver, v)
        time.sleep(4.2)
        cnt+=1
        if cnt % 30  == 0:
            time.sleep(10)
        if cnt % 100 == 0:
            output(en2ja)

    output(en2ja)
first()

#ソードアート 2がダメ