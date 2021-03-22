import numpy as np # linear algebra
import pandas as pd # pandas for dataframe based data processing and CSV file I/O

import requests # for http requests
from bs4 import BeautifulSoup # for html parsing and scraping
#from fastnumbers import isfloat
#from fastnumbers import fast_float
from multiprocessing.dummy import Pool as ThreadPool
import bs4

#import matplotlib.pyplot as plt
#import seaborn as sns
#import json
#from tidylib import tidy_document # for tidying incorrect html

from IPython.core.display import HTML

def get_table_simple(table,is_table_tag=True):
    elems = table.find_all('tr') if is_table_tag else get_children(table)
    table_data = list()
    for row in elems:

        row_data = list()
        row_elems = get_children(row)
        for elem in row_elems:
            text = elem.text.strip().replace("\n","").replace(",","")
            text = remove_multiple_spaces(text)
            if len(text)==0:
                text = 0.0
            row_data.append(text)
        table_data.append(row_data)
    return table_data

def get_children(html_content):
    children = list()
    for item in html_content.children:
        if type(item)==bs4.element.Comment:
            continue
        if type(item)==bs4.element.Tag or len(str(item).replace("\n","").strip())>0:
            children.append(item)

    return children

#def ffloat(string):
#    if string is None:
#        return np.nan
#    if type(string)==float or type(string)==np.float64:
#        return string
#    if type(string)==int or type(string)==np.int64:
#        return string
#    return fast_float(string.split(" ")[0].replace(',','').replace('%',''),
#                      default=np.nan)

#def ffloat_list(string_list):
#    return list(map(ffloat,string_list))

def remove_multiple_spaces(string):
    if type(string)==str:
        return ' '.join(string.split())
    return string

def request_with_check(url):
    page_response = requests.get(url, timeout=300)
    status = page_response.status_code
    if status>299:
        raise AssertionError("page content not found, status: %s"%status)
    return page_response

def findFullName_Screener(page_content):
    tag = (page_content.find("h1"))
    return tag.string


def findMarketCap_Screener(page_content):
    tag_str = str(page_content.find("li",attrs={'class':"flex flex-space-between"}))
    if "Market Cap" in tag_str:
        marcap = BeautifulSoup(tag_str)
        return(str(marcap.find("span",attrs={'class':"number"}).string) + " Cr.")
    else:
        return "0 INR Cr."

def findFullDescription_Screener(page_content):
    tag = page_content.find("div",attrs={'class':"company-profile-about"}).find("p")
    return tag.string

def findRatios_Screener(page_content):
    ratios_section = page_content.find("section",attrs={'id':"ratios"})
    ratios_table = ratios_section.find("table",attrs={'class':"data-table"})
    return get_table_simple(ratios_table, is_table_tag=True)

def findPandL_Screener(page_content):
    ratios_section = page_content.find("section",attrs={'id':"profit-loss"})
    ratios_table = ratios_section.find("table",attrs={'class':"data-table"})
    return get_table_simple(ratios_table, is_table_tag=True)

def findBalanceSheet_Screener(page_content):
    ratios_section = page_content.find("section",attrs={'id':"balance-sheet"})
    ratios_table = ratios_section.find("table",attrs={'class':"data-table"})
    return get_table_simple(ratios_table, is_table_tag=True)

def findCashFlow_Screener(page_content):
    ratios_section = page_content.find("section",attrs={'id':"cash-flow"})
    ratios_table = ratios_section.find("table",attrs={'class':"data-table"})
    return get_table_simple(ratios_table, is_table_tag=True)

def getPageContent_Screener(symbol):
    str1= "https://www.screener.in/company/" + symbol +"/consolidated/"
    page_response = requests.get(str1, timeout=300)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    return page_content

def findFullDescription(page_content, symbol):
    #page_content = getPageContent_Screener(symbol)
    return findFullDescription_Screener(page_content)

def findFullName(page_content, symbol):
    #page_content = getPageContent_Screener(symbol)
    return findFullName_Screener(page_content)

def findMarketCap(page_content, symbol):
    #page_content = getPageContent_Screener(symbol)
    return findMarketCap_Screener(page_content)

def findRatios(page_content, symbol):
    #page_content = getPageContent_Screener(symbol)
    return findRatios_Screener(page_content)

def findPandL(page_content, symbol):
    #page_content = getPageContent_Screener(symbol)
    return findPandL_Screener(page_content)

def findBalanceSheet(page_content, symbol):
    #page_content = getPageContent_Screener(symbol)
    return findBalanceSheet_Screener(page_content)

def findCashFlow(page_content, symbol):
    #page_content = getPageContent_Screener(symbol)
    return findCashFlow_Screener(page_content)
