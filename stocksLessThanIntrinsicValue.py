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

from getWeeklyMA_yf import getWMAandRSI
from nsetools import Nse  # Nse Driver

import sys, getopt
from findIntrinsicValue import findIntrinsicValue

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
    leng = len(listOfStocks)
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

def doesRoceDataMeetCriteria(roce_info, threshold, strict=True):
    if strict == True:
        if len(roce_info) == 0:
            return False
        return all(i >= threshold for i in roce_info)
    else:
        return (Average(roce_info) >= threshold)

def doesSalesDataMeetCriteria(sales_info, threshold, strict=True):
    if strict == True:
        if len(sales_info) == 0:
            return False
        return all(i >= threshold for i in sales_info)
    else:
        return (Average(sales_info) >= threshold)




def checkForCoffeeCanInvestingStocks(dictCap, cap='Large',  roceThreshold=15, salesThreshold=10, mask1=False, mask2=False, strict=True):
    coffeeCanPortfolio = []
    nse = Nse()
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
        isRoceCriteriaMatch = doesRoceDataMeetCriteria(roce_info, roceThreshold, strict)
        sales_info = getSalesGrowthForTheStock(stockInfo)
        isSalesCriteriaMatch = doesSalesDataMeetCriteria(sales_info, salesThreshold, strict)
        if (isRoceCriteriaMatch or mask1) and (isSalesCriteriaMatch or mask2):
            stockInfo.insert(0, symbol)
            stockInfo.append(Average(roce_info))
            stockInfo.append(Average(sales_info))
            if True: #cap == 'Large':
                wma, rsi, cmp, dir  = getWMAandRSI(symbol)
                q = nse.get_quote(symbol)
                if q is not None:
                    h52 =  q['high52']
                else:
                    h52 = 0.0
                if cmp > 0:
                    upp = ((h52-cmp)/(cmp))*100.00
                    risk = ((cmp-wma)/cmp)*100.00
                else:
                    upp = 0.0
                    risk = 0.0
            else:
                wma, rsi, cmp = 0.0, 0.0, 0.0
                stockInfo.append(rsi)
                stockInfo.append(cmp)
                stockInfo.append(wma)
                h52 = 0.0
                upp = 0.0
                risk = 0.0
            stockInfo.append(rsi)
            stockInfo.append(cmp)
            stockInfo.append(wma)
            stockInfo.append(h52)
            stockInfo.append(upp)
            stockInfo.append(risk)

            #print(roce_info)
            #print(sales_info)
            coffeeCanPortfolio.append(stockInfo)

    return coffeeCanPortfolio




import sys

def checkForIntrinsicStocks(dictCap, cap='Large'):
    coffeeCanPortfolio = []
    nse = Nse()
    largeCapList = list(dictCap.keys())
    #print(largeCapList)
    #print("Total ",cap ," Stocks: ", len(largeCapList))
    for i in range(0, len(largeCapList),1):
        #print(i)
        #print(largeCapList[i])
        symbol = largeCapList[i]
        print(symbol)
        #stockInfo = getDataForTheStock(dictCap, symbol)
        try:
            stockInfo = getDataForTheStock(dictCap, symbol)
            intrinsic_price, price = findIntrinsicValue(stock = symbol, standalone=False)
            if(intrinsic_price == 0.0):
                intrinsic_price, price = findIntrinsicValue(stock = symbol, standalone=True)
        except:
             print("Whew!", sys.exc_info()[0], "occurred.")
             continue

        #print(stockInfo)
        roce_info = getROCEForTheStock(stockInfo)
        #print(roce_info)
        #isRoceCriteriaMatch = doesRoceDataMeetCriteria(roce_info, roceThreshold, strict)
        sales_info = getSalesGrowthForTheStock(stockInfo)
        #isSalesCriteriaMatch = doesSalesDataMeetCriteria(sales_info, salesThreshold, strict)
        if (intrinsic_price > price) and (intrinsic_price > 0.0 ):
            stockInfo.insert(0, symbol)
            stockInfo.append(Average(roce_info))
            stockInfo.append(Average(sales_info))
            if True: #cap == 'Large':
                try:
                    wma, rsi, cmp, dir  = getWMAandRSI(symbol)
                    q = nse.get_quote(symbol)
                except:
                    q = None
                    wma = 0.0
                    rsi = 0.0
                    cmp = 0.0
                    dir = 'UP'
                if q is not None:
                    h52 =  q['high52']
                else:
                    h52 = 0.0
                if cmp > 0:
                    upp = ((h52-cmp)/(cmp))*100.00
                    risk = ((cmp-wma)/cmp)*100.00
                else:
                    upp = 0.0
                    risk = 0.0
            else:
                wma, rsi, cmp = 0.0, 0.0, 0.0
                stockInfo.append(rsi)
                stockInfo.append(cmp)
                stockInfo.append(wma)
                h52 = 0.0
                upp = 0.0
                risk = 0.0
            stockInfo.append(rsi)
            stockInfo.append(cmp)
            stockInfo.append(wma)
            stockInfo.append(h52)
            stockInfo.append(upp)
            stockInfo.append(risk)
            stockInfo.append(intrinsic_price)

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
    print("%4s %15s %45s %10s %10s %10s %10s %10s %10s %10s %10s"%("No","Symbol", "Name", "Intrs.Val", "ROCE % (Avg)", "Sales Gr % (Avg)", "   RSI", " CMP " , " %UpPotential", " %RiskMargin", " Ratio"))
    cnt = 1
    for i in port:
        #print(i)
        #print(i[7])
        if i[15] != 0.0:
            ratio = i[14]/i[15]
        else:
            ratio = 0.0

        print("%4s %15s %45s %8.2f  %8.2f     %8.2f           %8.2f    %8.2f    %8.2f    %8.2f    %8.2f"%(cnt, i[0], i[1],i[16], i[8], i[9], i[10],i[11],i[14],i[15],ratio))
        cnt = cnt+1
    print("------------------------------------------------------------------")
    return

def my_main(argv):

    ### USE THIS TO BUILD THE DATABASE
    #pprint(getAllTheStocksInfo('LARGE', True))
    #pprint(getAllTheStocksInfo('MID', True))
    #pprint(getAllTheStocksInfo('SMALL', True))
    try:
      opts, args = getopt.getopt(argv,"$hlmsS:R:")
    except getopt.GetoptError:
      print( 'stocksLessThanInstrinsicValue.py -h -l -m -s ')
      sys.exit(2)

    [dictLargeCap, dictMidCap, dictSmallCap] =  getAllCapStocks(False)

    def_dict = dictLargeCap
    cap = 'Large'

    for opt, arg in opts:
        if opt == '-h':
            print ('stocksLessThanInstrinsicValue.py -h -l -m -s ')
            sys.exit()
        elif opt in ("-m"):
            def_dict = dictMidCap
            cap = 'Mid'
        elif opt in ("-s"):
            def_dict = dictSmallCap
            cap = 'Small'




    ccp = checkForIntrinsicStocks(def_dict, cap)
    print("Number of CCP Stocks :", len(ccp))
    printPortfolio(ccp)




if __name__ == '__main__':
    my_main(sys.argv[1:])
