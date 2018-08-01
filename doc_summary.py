# -*- coding: utf-8 -*-

"""
Created on Sat Jul 21 01:53:23 2018
https://arxiv.org/abs/1602.03606
document summarization
@author: Thinkpad
Yandex key: "trnsl.1.1.20180721T105414Z.d2f019e156566dca.6f5f0ae60b8ea34ad5ee3dc2e6b85f6b642f3f86"
"""

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)
import pandas as pd
from gensim.summarization import summarize
import requests
from lxml import html
import json
from tkinter import *
from my_layout import *

def sumarize(text):
    # summarize text in English
    sumtext = summarize(text, word_count = 30)
    print(sumtext)
    return (sumtext)

def creat_gui(df_all_data):
    
    root = Tk()   
    height = df_all_data.shape[0]
    width = df_all_data.shape[1]
    for i in range(height): #Rows
        for j in range(width): #Columns
            b = Entry(root, text="")
            b.grid(row=i, column=j)
            #b.pack()
    mainloop()
    
def translate(text, trans_direction):
    # translate text from English to VietNamese
    api_key = "trnsl.1.1.20180721T105414Z.d2f019e156566dca.6f5f0ae60b8ea34ad5ee3dc2e6b85f6b642f3f86"
    link = "https://translate.yandex.net/api/v1.5/tr.json/translate?"
    r = requests.post(link, data={'lang': trans_direction, 'key': api_key, 'text': text})
    try:
        k = json.loads(r.text)['text'][0]
        return (k)
    except:
        return("None")

def scrap_article_links():
    link = "https://smartfarmerkenya.com/category/how-to/"
    xpath = "//h3[@class = 'entry-title td-module-title']/a"
    
    page = requests.get(link)
    tree = html.document_fromstring(page.content)        
    pages = [e.get("href") for e in tree.xpath(xpath)]
    
    df_all_data = pd.DataFrame()
    title_list = []
    content_list = []
    vn_title_list = []
    vn_summary_list = []
    page_list = []
    
    for page in pages[0:5]:
        tree2 = html.document_fromstring(requests.get(page).content)
        article_title = tree2.xpath("//h1[@class = 'entry-title']")[0].text_content()
        cont = [e.text_content() for e in tree2.xpath("//p")]
        article_content = " ".join(cont)
        sum_content = sumarize(article_content)
        
        vn_title = translate(article_title, "en-vi")
        vn_sum_content = translate(sum_content, "en-vi")
        if(vn_title != "None" and vn_sum_content != "None"):
            vn_title_list.append(vn_title)
            vn_summary_list.append(vn_sum_content)
            page_list.append(page)
        
        title_list.append(article_title)
        content_list.append(article_content)
    
    df_data = pd.DataFrame({'title': vn_title_list, 'summary': vn_summary_list, "link": page_list})
    print(df_data.head(n = 5))
    return(df_data)

if __name__ == '__main__':
    df_data = scrap_article_links()
    cols = ['Title', 'Summary', 'Link']
    rows = range(df_data.shape[0])
    app = EntryGrid(cols, rows, df_data)

