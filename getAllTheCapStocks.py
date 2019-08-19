'''
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
'''
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


#Assumes the dict file exists
def getAllTheLargeCapStocks(overrule=False):
    if True:
        #Read the file
        s = open('dictLargeCap.txt', 'r').read()
        #Create the dictionary
        dictLargeCap = eval(s)
        #Return the dict
        return dictLargeCap



#Assumes the dict file exists
def getAllTheSmallCapStocks(overrule=False):
    if True:
        #Read the file
        s = open('dictSmallCap.txt', 'r').read()
        #Create the dictionary
        dictSmallCap = eval(s)
        #Return the dict
        return dictSmallCap



def getAllTheMidCapStocks(overrule=False):
    if True:
        #Read the file
        s = open('dictMidCap.txt', 'r').read()
        #Create the dictionary
        dictMidCap = eval(s)
        #Return the dict
        return dictMidCap




#Assumes the dict file exists
def getAllCapStocks(overrule=False):
    if True:
        #Read the file
        s = open('dictMidCap.txt', 'r').read()
        #Create the dictionary
        dictMidCap = eval(s)
        needMidCap = False
    if True:
        #Read the file
        s = open('dictSmallCap.txt', 'r').read()
        #Create the dictionary
        dictSmallCap = eval(s)
        needSmallCap = False
    if True:
        #Read the file
        s = open('dictLargeCap.txt', 'r').read()
        #Create the dictionary
        dictLargeCap = eval(s)
        needLargeCap = False

    return [ dictLargeCap, dictMidCap, dictSmallCap]





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
    return sum(lst) / len(lst)
