from getAllStocksCodesNse import getListOfNseStocks
from getAllStocksCodesNse import getTotalOfNseStocks
from pprint import pprint # just for neatness of display
from WebScrapperRoutines import findFullDescription
from WebScrapperRoutines import findFullName
from WebScrapperRoutines import findMarketCap
from WebScrapperRoutines import findRatios
from WebScrapperRoutines import findPandL
from WebScrapperRoutines import findBalanceSheet
from WebScrapperRoutines import findCashFlow
from WebScrapperRoutines import getPageContent_Screener

import os.path
from os import path
import numpy as np # linear algebra
import pandas as pd # pandas for dataframe based data processing and CSV file I/O

def is_number_tryexcept(s):
    """ Returns True is string is a number. """
    try:
        float(s)
        return True
    except ValueError:
        return False



def getAllTheLargeCapStocks(overrule=False):
    if path.exists('dictLargeCap.txt'):
        #Read the file
        s = open('dictLargeCap.txt', 'r').read()
        #Create the dictionary
        dictLargeCap = eval(s)
        #Return the dict
        if not overrule:
            return dictLargeCap
        

    #listOfNse = getListOfNseStocks(verbose=False)
    listOfStocks = list(getListOfNseStocks(verbose=False).keys())
    leng = len(listOfStocks)
    dictLargeCap = {}
    #print("Range : ", leng)
    
    for i in range(1,leng,1):
        stock = listOfStocks[i]
        page_content = getPageContent_Screener(stock)
        symbol = stock
        print("Symbol : ", symbol)
        fullName = findFullName(page_content, stock)
        print("Full Name : ", fullName)
        desc = findFullDescription(page_content, stock)
        print("Full Desc : ", desc)
        marketCap = (findMarketCap(page_content, stock).split())[0].replace(",", "")
        if is_number_tryexcept(marketCap):
            marketCap = float(marketCap)
        else:
            marketCap = 0.0
        print("Market Cap : ", marketCap)
        isLargeCap = (marketCap >= 20000.0)
        print("Is Large Cap :", isLargeCap)
        ratios = findRatios(page_content, stock)
        pAndL = findPandL(page_content, stock)
        balanceSheet = findBalanceSheet(page_content, stock)
        cashFlow = findCashFlow(page_content, stock)
        if isLargeCap:
            dictLargeCap[symbol] = [fullName, desc, marketCap, pAndL, balanceSheet, cashFlow, ratios]
    
    targetFile = open('dictLargeCap.txt', 'w')
    targetFile.write(str(dictLargeCap))
    
    return dictLargeCap
    

def getAllTheSmallCapStocks(overrule=False):
    if path.exists('dictSmallCap.txt'):
        #Read the file
        s = open('dictSmallCap.txt', 'r').read()
        #Create the dictionary
        dictSmallCap = eval(s)
        #Return the dict
        if not overrule:
            return dictSmallCap
        

    #listOfNse = getListOfNseStocks(verbose=False)
    listOfStocks = list(getListOfNseStocks(verbose=False).keys())
    leng = len(listOfStocks)
    dictSmallCap = {}
    #print("Range : ", leng)
    
    for i in range(1,leng,1):
        stock = listOfStocks[i]
        page_content = getPageContent_Screener(stock)
        symbol = stock
        print("Symbol : ", symbol)
        fullName = findFullName(page_content, stock)
        print("Full Name : ", fullName)
        desc = findFullDescription(page_content, stock)
        print("Full Desc : ", desc)
        marketCap = (findMarketCap(page_content, stock).split())[0].replace(",", "")
        if is_number_tryexcept(marketCap):
            marketCap = float(marketCap)
        else:
            marketCap = 0.0
        print("Market Cap : ", marketCap)
        ratios = findRatios(page_content, stock)
        pAndL = findPandL(page_content, stock)
        balanceSheet = findBalanceSheet(page_content, stock)
        cashFlow = findCashFlow(page_content, stock)
        isSmallCap = (marketCap <= 1000.0)
        print("Is Small Cap :", isSmallCap)
        if isSmallCap:
            dictSmallCap[symbol] = [fullName, desc, marketCap, pAndL, balanceSheet, cashFlow, ratios]
    
    targetFile = open('dictSmallCap.txt', 'w')
    targetFile.write(str(dictSmallCap))
    
    return dictSmallCap

def getAllTheMidCapStocks(overrule=False):
    if path.exists('dictMidCap.txt'):
        #Read the file
        s = open('dictMidCap.txt', 'r').read()
        #Create the dictionary
        dictMidCap = eval(s)
        #Return the dict
        if not overrule:
            return dictMidCap
        

    #listOfNse = getListOfNseStocks(verbose=False)
    listOfStocks = list(getListOfNseStocks(verbose=False).keys())
    leng = len(listOfStocks)
    dictMidCap = {}
    #print("Range : ", leng)
    
    for i in range(1,leng,1):
        stock = listOfStocks[i]
        page_content = getPageContent_Screener(stock)
        symbol = stock
        print("Symbol : ", symbol)
        fullName = findFullName(page_content, stock)
        print("Full Name : ", fullName)
        desc = findFullDescription(page_content, stock)
        print("Full Desc : ", desc)
        marketCap = (findMarketCap(page_content, stock).split())[0].replace(",", "")
        if is_number_tryexcept(marketCap):
            marketCap = float(marketCap)
        else:
            marketCap = 0.0
        print("Market Cap : ", marketCap)
        ratios = findRatios(page_content, stock)
        pAndL = findPandL(page_content, stock)
        balanceSheet = findBalanceSheet(page_content, stock)
        cashFlow = findCashFlow(page_content, stock)
        isMidCap = ((marketCap > 1000.0) & (marketCap < 20000.0))
        print("Is Mid Cap :", isMidCap)
        if isMidCap:
            dictMidCap[symbol] = [fullName, desc, marketCap, pAndL, balanceSheet, cashFlow, ratios]
    
    targetFile = open('dictMidCap.txt', 'w')
    targetFile.write(str(dictMidCap))
    
    return dictMidCap

def getAllTheStocksInfo(cap='LARGE', force=False):
    if cap is 'LARGE':
        return getAllTheLargeCapStocks(overrule=force)
    if cap is 'SMALL':
        return getAllTheSmallCapStocks(overrule=force)
    if cap is 'MID':
        return getAllTheMidCapStocks(overrule=force)

def getDataForTheStock(dictOfStocks, symbol):
    return dictOfStocks[symbol]

def getROCEForTheStock(stockInfo):
    table = stockInfo[6]
    #print(table)
    #table[0].insert(0,'None')
    #print(table)
    frame = pd.DataFrame(table)    
    print(frame)
    lol = frame.values.tolist()
    temp =  lol[1][1:] 
    for i in range(0,len(temp),1):
        if '%' in temp[i]:
            temp[i].replace('%','')
        if is_number_tryexcept(temp[i]):
            temp[i] = float(temp[i])
        else:
            temp[i] = 0.0
    a = temp #[float(x[:-1]) for x in temp]
    return a

def doesRoceDataMeetCriteria(roce_info, threshold):
    return all(i >= threshold for i in roce_info)


def checkForCoffeeCanInvestingStocks(dictLargeCap):
    coffeeCanPortfolio = []
    largeCapList = list(dictLargeCap.keys())
    #print(largeCapList)
    print("Total LargeCap Stocks: ", len(largeCapList))
    for i in range(5,len(largeCapList),1):
        #print(i)
        #print(largeCapList[i])
        symbol = largeCapList[i]
        stockInfo = getDataForTheStock(dictLargeCap, symbol)
        #print(stockInfo)
        roce_info = getROCEForTheStock(stockInfo)
        #print(roce_info)
        isRoceCriteriaMatch = doesRoceDataMeetCriteria(roce_info, 15)
        if isRoceCriteriaMatch:
            coffeeCanPortfolio.append(stockInfo)
    
    return coffeeCanPortfolio

# USE THIS TO BUILD THE DATABASE        
pprint(getAllTheStocksInfo('LARGE', True))
pprint(getAllTheStocksInfo('MID', True))
pprint(getAllTheStocksInfo('SMALL', True))
    
   
#dictLargeCap = getAllTheStocksInfo('LARGE', False)
#ccp = checkForCoffeeCanInvestingStocks(dictLargeCap)
#print("Number of CCP Stocks :", len(ccp))