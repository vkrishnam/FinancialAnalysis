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
from statistics import mean

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

import time

def getAllCapStocks_selectively(overrule=False):


    if path.exists('dictMidCap.txt') and (overrule == False):
        #Read the file
        s = open('dictMidCap.txt', 'r').read()
        #Create the dictionary
        dictMidCap = eval(s)
        needMidCap = False
    else:
        dictMidCap = {}
        needMidCap = True

    if path.exists('dictSmallCap.txt') and (overrule == False):
        #Read the file
        s = open('dictSmallCap.txt', 'r').read()
        #Create the dictionary
        dictSmallCap = eval(s)
        needSmallCap = False
    else:
        dictSmallCap = {}
        needSmallCap = True

    if path.exists('dictLargeCap.txt') and (overrule == False):
        #Read the file
        s = open('dictLargeCap.txt', 'r').read()
        #Create the dictionary
        dictLargeCap = eval(s)
        needLargeCap = False
    else:
        dictLargeCap = {}
        needLargeCap = True

    #if( (not needLargeCap) and (not needMidCap) and (not needSmallCap) ):
    #   return [ dictLargeCap, dictMidCap, dictSmallCap]

    #listOfNse = getListOfNseStocks(verbose=False)
    listOfStocks = list(getListOfNseStocks(verbose=False).keys())

    #listOfStocks.remove("A2ZINFRA")



    leng = len(listOfStocks)
    #print("Range : ", leng)




    for i in range(1,leng,1):
        stock = listOfStocks[i]

        symbol = stock
        print("Symbol : ", symbol)

        #time.sleep(2)

        #check if the symbol is already in dictionaries
        # else go for web scrapping

        if (symbol in dictLargeCap.keys()) or (symbol in dictMidCap.keys()) or (symbol in dictSmallCap.keys()):
            continue



        try:
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
            isLargeCap = ((marketCap >= 20000.0))
            isSmallCap = ((marketCap <= 1000.0))
            print("Is Mid Cap :", isMidCap)
            print("Is Small Cap :", isSmallCap)
            print("Is Large Cap :", isLargeCap)
            if isMidCap:
                dictMidCap[symbol] = [fullName, desc, marketCap, pAndL, balanceSheet, cashFlow, ratios]
                #if needMidCap:
                targetFile = open('dictMidCap.txt', 'w')
                targetFile.write(str(dictMidCap))
                targetFile.close()
            if isSmallCap:
                dictSmallCap[symbol] = [fullName, desc, marketCap, pAndL, balanceSheet, cashFlow, ratios]
                #if needSmallCap:
                targetFile = open('dictSmallCap.txt', 'w')
                targetFile.write(str(dictSmallCap))
                targetFile.close()
            if isLargeCap:
                dictLargeCap[symbol] = [fullName, desc, marketCap, pAndL, balanceSheet, cashFlow, ratios]
                #if needLargeCap:
                targetFile = open('dictLargeCap.txt', 'w')
                targetFile.write(str(dictLargeCap))
                targetFile.close()
            time.sleep(30)
        except:
            continue


    return [dictLargeCap,dictMidCap,dictSmallCap]



def getAllCapStocks(overrule=False):
    if path.exists('dictMidCap.txt') and (overrule == False):
        #Read the file
        s = open('dictMidCap.txt', 'r').read()
        #Create the dictionary
        dictMidCap = eval(s)
        needMidCap = False
    else:
        dictMidCap = {}
        needMidCap = True
    if path.exists('dictSmallCap.txt') and (overrule == False):
        #Read the file
        s = open('dictSmallCap.txt', 'r').read()
        #Create the dictionary
        dictSmallCap = eval(s)
        needSmallCap = False
    else:
        dictSmallCap = {}
        needSmallCap = True
    if path.exists('dictLargeCap.txt') and (overrule == False):
        #Read the file
        s = open('dictLargeCap.txt', 'r').read()
        #Create the dictionary
        dictLargeCap = eval(s)
        needLargeCap = False
    else:
        dictLargeCap = {}
        needLargeCap = True

    if( (not needLargeCap) and (not needMidCap) and (not needSmallCap) ):
        return [ dictLargeCap, dictMidCap, dictSmallCap]

    #listOfNse = getListOfNseStocks(verbose=False)
    listOfStocks = list(getListOfNseStocks(verbose=False).keys())

    listOfStocks.remove("A2ZINFRA")



    leng = len(listOfStocks)
    #print("Range : ", leng)




    for i in range(1,leng,1):
        stock = listOfStocks[i]
        try:
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
            isLargeCap = ((marketCap >= 20000.0))
            isSmallCap = ((marketCap <= 1000.0))
            print("Is Mid Cap :", isMidCap)
            print("Is Small Cap :", isSmallCap)
            print("Is Large Cap :", isLargeCap)
            if isMidCap and  needMidCap:
                dictMidCap[symbol] = [fullName, desc, marketCap, pAndL, balanceSheet, cashFlow, ratios]
            if isSmallCap and needSmallCap:
                dictSmallCap[symbol] = [fullName, desc, marketCap, pAndL, balanceSheet, cashFlow, ratios]
            if isLargeCap and  needLargeCap:
                dictLargeCap[symbol] = [fullName, desc, marketCap, pAndL, balanceSheet, cashFlow, ratios]
        except:
            continue

    if needMidCap:
        targetFile = open('dictMidCap.txt', 'w')
        targetFile.write(str(dictMidCap))
    if needSmallCap:
        targetFile = open('dictSmallCap.txt', 'w')
        targetFile.write(str(dictSmallCap))
    if needLargeCap:
        targetFile = open('dictLargeCap.txt', 'w')
        targetFile.write(str(dictLargeCap))

    return [dictLargeCap,dictMidCap,dictSmallCap]



def getAllTheStocksInfo(cap='LARGE', force=False):
    if cap == 'LARGE':
        return getAllTheLargeCapStocks(overrule=force)
    if cap == 'SMALL':
        return getAllTheSmallCapStocks(overrule=force)
    if cap == 'MID':
        return getAllTheMidCapStocks(overrule=force)

def getDataForTheStock(dictOfStocks, symbol):
    return dictOfStocks[symbol]


def getSalesForTheStock(stockInfo):
    table = stockInfo[3]
    frame = pd.DataFrame(table)
    lol = frame.values.tolist()
    temp =  lol[1][1:]
    for i in range(0,len(temp),1):
        temp[i] = str(temp[i])
        if is_number_tryexcept(temp[i]):
            #print("Y1 ", i)
            temp[i] = float(temp[i])
        else:
            #print("Y2 ", i)
            temp[i] = 0.0
    a = temp #[float(x[:-1]) for x in temp]
    return a

def getSalesGrowthForTheStock(stockInfo):
    sales = getSalesForTheStock(stockInfo)
    sales_growth = []
    for i in range(1,len(sales),1):
        diff = sales[i] - sales[i-1]
        if sales[i-1] != 0.0:
            percentage = (diff*100)/sales[i-1]
        else:
            percentage = 0.0
        sales_growth.append(percentage)
    return sales_growth


def getROCEForTheStock(stockInfo):
    table = stockInfo[6]
    #print(table)
    #table[0].insert(0,'None')
    #print(table)
    frame = pd.DataFrame(table)
    #print(frame)
    lol = frame.values.tolist()
    temp =  lol[1][1:]
    #print("Hello")
    #print(temp)
    #print(len(temp))
    for i in range(0,len(temp),1):
        temp[i] = str(temp[i])
        #print(temp[i])
        if '%' in temp[i]:
            #print("Y0 ", i)
            temp[i] = temp[i].replace('%','')
            #print(temp[i])
        if is_number_tryexcept(temp[i]):
            #print("Y1 ", i)
            temp[i] = float(temp[i])
        else:
            #print("Y2 ", i)
            temp[i] = 0.0
    a = temp #[float(x[:-1]) for x in temp]
    return a

def doesRoceDataMeetCriteria(roce_info, threshold):
    #print(roce_info)
    if len(roce_info) == 0:
        return False
    return all(i >= threshold for i in roce_info)

def doesSalesDataMeetCriteria(sales_info, threshold):
    #print(roce_info)
    if len(sales_info) == 0:
        return False
    return all(i >= threshold for i in sales_info)

def checkForCoffeeCanInvestingStocks(dictCap, cap='Large',  roceThreshold=15, salesThreshold=10, mask1=False, mask2=False):
    coffeeCanPortfolio = []
    largeCapList = list(dictCap.keys())
    #print(largeCapList)
    #print("Total ",cap ," Stocks: ", len(largeCapList))
    for i in range(0, len(largeCapList),1):
        #print(i)
        #print(largeCapList[i])
        symbol = largeCapList[i]
        stockInfo = getDataForTheStock(dictCap, symbol)
        #print(stockInfo)
        roce_info = getROCEForTheStock(stockInfo)
        #print(roce_info)
        isRoceCriteriaMatch = doesRoceDataMeetCriteria(roce_info, roceThreshold)
        sales_info = getSalesGrowthForTheStock(stockInfo)
        isSalesCriteriaMatch = doesSalesDataMeetCriteria(sales_info, salesThreshold)
        if (isRoceCriteriaMatch or mask1) and (isSalesCriteriaMatch or mask2):
            stockInfo.insert(0, symbol)
            stockInfo.append(Average(roce_info))
            stockInfo.append(Average(sales_info))
            #print(roce_info)
            #print(sales_info)
            coffeeCanPortfolio.append(stockInfo)

    return coffeeCanPortfolio

def Average(lst):
    #print(lst)
    #print(type(lst))
    #print(sum(lst))
    #print(len(lst))
    if len(lst):
        return sum(lst) / len(lst)
    else:
        return 0.0

def printPortfolio(port):
    print("------------------------------------------------------------------")
    print("                       Portfolio ")
    print("------------------------------------------------------------------")
    print("%4s %15s %45s %10s %10s"%("No","Symbol", "Name", "ROCE % (Avg)", "Sales Gr % (Avg)"))
    cnt = 1
    for i in port:
        #print(i)
        #print(i[7])
        print("%4s %15s %45s %8.2f %8.2f"%(cnt, i[0], i[1], i[8], i[9]))
        cnt = cnt+1
    print("------------------------------------------------------------------")
    return

def my_main():

    ### USE THIS TO BUILD THE DATABASE
    #pprint(getAllTheStocksInfo('LARGE', True))
    #pprint(getAllTheStocksInfo('MID', True))
    #pprint(getAllTheStocksInfo('SMALL', True))

    #[dictLargeCap, dictMidCap, dictSmallCap] =  getAllCapStocks(False)
    [dictLargeCap, dictMidCap, dictSmallCap] =  getAllCapStocks_selectively(False)

    ccp = checkForCoffeeCanInvestingStocks(dictLargeCap, 'Large', 15, 10, False, True)
    print("Number of CCP Stocks :", len(ccp))
    printPortfolio(ccp)

    ccp = checkForCoffeeCanInvestingStocks(dictMidCap, 'Mid', 15, 10, False, True)
    print("Number of CCP Stocks :", len(ccp))
    printPortfolio(ccp)

    ccp = checkForCoffeeCanInvestingStocks(dictSmallCap, 'Small', 15, 10, False, True)
    print("Number of CCP Stocks :", len(ccp))
    printPortfolio(ccp)



if __name__ == '__main__':
    my_main()
