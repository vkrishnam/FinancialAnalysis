
from getAllStocksCodesNse import getListOfNseStocks
from getAllStocksCodesNse import getTotalOfNseStocks
from pprint import pprint # just for neatness of display
from WebScrapperRoutines import findFullDescription
from WebScrapperRoutines import findFullName
from WebScrapperRoutines import findFaceValue
from WebScrapperRoutines import findMarketCap
from WebScrapperRoutines import findRatios
from WebScrapperRoutines import findPE
from WebScrapperRoutines import findDividendYield
from WebScrapperRoutines import findROCE
from WebScrapperRoutines import findROE
from WebScrapperRoutines import findPandL
from WebScrapperRoutines import findBalanceSheet
from WebScrapperRoutines import findCashFlow
from WebScrapperRoutines import getPageContent_Screener
from WebScrapperRoutines import getPageContent_Standalone_Screener
from statistics import mean

import os.path
from os import path
import numpy as np # linear algebra
import pandas as pd # pandas for dataframe based data processing and CSV file I/O


def getCashFlowStatement(page_content,verbose=True):
    table = findCashFlow(page_content)
    table[0][0] = "Index"
    #print(table)
    #print("\n\n")
    df  = pd.DataFrame(table[1:], columns=table[0]).set_index('Index')
    if verbose:
        print("Cash Flow Statement")
        print(df)
    return df

def getPandLStatement(page_content,verbose=True):
    table = findPandL(page_content)
    table[0][0] = "Index"
    #print(table)
    #print("\n\n")
    df  = pd.DataFrame(table[1:], columns=table[0]).set_index('Index')
    if verbose:
        print("P&L Statement")
        print(df)
    return df

def getBalanceSheetStatement(page_content,verbose=True):
    table = findBalanceSheet(page_content)
    table[0][0] = "Index"
    #print(table)
    #print("\n\n")
    df  = pd.DataFrame(table[1:], columns=table[0]).set_index('Index')
    if verbose:
        print("Balance Sheet Statement")
        print(df)
    return df

from yahoo_fin import stock_info as si

from bsedata.bse import BSE
import datetime

def findStickerPrice(stock = 'IEX', standalone = False,verbose=True):
    if standalone:
        page_content = getPageContent_Standalone_Screener(stock)
    else:
        page_content = getPageContent_Screener(stock)
    if page_content ==  None:
        return 0.0, 0.0
    symbol = stock
    #print("\nSymbol : ", symbol)
    fullName = findFullName(page_content, stock)
    #print("\nFull Name : ", fullName)
    desc = findFullDescription(page_content, stock)
    #print("\nFull Desc : ", desc)
    face = findFaceValue(page_content, stock)
    #print("\nFace Value  : ", face)
    roce = findROCE(page_content, stock)
    print("\nROCE  : ", roce)
    roe = findROE(page_content, stock)
    #print("\nROE  : ", roe)
    pe = findPE(page_content, stock)
    print("\nPE  : ", pe)
    dy = findDividendYield(page_content, stock)
    #print("\nDividend Yield  : ", dy)

    #f = open("filecontent.html", 'w')
    #f.write(str(page_content));
    #f.close()
    #print('Debug:::: '+str(stock)+'.NS')

    #is numeral
    if stock.isdigit():
        b = BSE(update_codes = True)
        q = b.getQuote(stock)
        #print(q)
        price = q["currentValue"]
    else:
        price = si.get_live_price(str(stock)+'.NS')

    discount_rate = 9
    first_five = 15
    next_five = 10
    terminal = 5
    term = 10
    num_years_data = 5
    today = datetime.date.today()

    year = today.year
    #print(year)
    current_year  = year

    cash_from_operations = []
    capex = []
    free_cash_flow = []
    eps = []
    equity = []
    sales = []


    df_cash_flow = getCashFlowStatement(page_content,verbose)
    df_PandL = getPandLStatement(page_content,verbose)
    df_bSheet = getBalanceSheetStatement(page_content,verbose)

    #print(df_bSheet)

    if 'TTM' in df_PandL.columns:
        df_PandL = df_PandL.drop(['TTM'],axis = 1)
    if 'TTM' in df_cash_flow.columns:
        df_cash_flow = df_cash_flow.drop(['TTM'],axis = 1)
    if 'TTM' in df_bSheet.columns:
        df_bSheet = df_bSheet.drop(['TTM'],axis = 1)
    number_of_years_avail = len(df_PandL.columns)
    #print('Number of years : '+str(number_of_years_avail))
    #return 0.0 , 0.0

    years = df_PandL.columns

    #print(years)

    months = ['Mar ', 'Dec ']
    #year  = current_year
    year = 'Mar '+str(current_year)
    fixed_month = 'Mar '
    found_match = False

    #print(df_cash_flow.columns)

    for month in months:
        year1 = month + str(current_year)
        year2 = month + str(current_year-1)
        #print(year1, year2)
        if year1 in df_cash_flow.columns:
            fixed_month = month
            found_match = True
            year = year1
            break;
        if year2 in df_cash_flow.columns:
            fixed_month = month
            found_match = True
            year = year2
            break

    if found_match == False:
        current_year = 2020
        for month in months:
            year = month + str(current_year)
            if year in df_cash_flow.columns:
                fixed_month = month
                found_match = True
                break;
    if found_match == False:
        print("prob")
        return 0.0, 0.0

    #print(fixed_month)
    #print(current_year)

    if verbose:
        print('Symbol : ' + symbol)
    #print(year+"\n ")
    #print(df_bSheet)
    #print("Venu\n")

    #total_debt = float(df_bSheet.at['Borrowings', year])
    share_capital = float(df_bSheet.at['Share Capital -', year])
    cash_cash_balance = float(df_bSheet.at['Cash Equivalents', year])



    future_cash_flow = []
    future_disc_cash_flow = []


    number_of_years_avail = min(11, number_of_years_avail)

    #print(number_of_years_avail)

    for i in range(number_of_years_avail):
        year  = current_year - i
        year =  fixed_month +str(year)
        year = years[-1*i-1]

        #print(year)
        if 'Cash from Operating Activity -' in df_cash_flow.index:
            if year in df_cash_flow.columns:
                cashFromOperatingActivity  = (df_cash_flow.at['Cash from Operating Activity -', year])
                cash_from_operations.append(float(cashFromOperatingActivity))
            else:
                cash_from_operations.append(0.0)
        else:
            cash_from_operations.append(0.0)

        if 'Net Cash Flow' in df_cash_flow.index:
            if year in df_cash_flow.columns:
                cashFromOperatingActivity  = (df_cash_flow.at['Net Cash Flow', year])
                free_cash_flow.append(float(cashFromOperatingActivity))
            else:
                free_cash_flow.append(0.0)
        else:
            free_cash_flow.append(0.0)

        if 'Sales +' in df_PandL.index:
            if year in df_PandL.columns:
                cashFromOperatingActivity  = (df_PandL.at['Sales +', year])
                sales.append(float(cashFromOperatingActivity))
            else:
                sales.append(0.0)
        else:
            sales.append(0.0)

        if 'EPS in Rs' in df_PandL.index:
            if year in df_PandL.columns:
                cashFromOperatingActivity  = (df_PandL.at['EPS in Rs', year])
                eps.append(float(cashFromOperatingActivity))
            else:
                eps.append(0.0)
        else:
            eps.append(0.0)

        ee = 0.0

        #if 'Total Assets' in df_bSheet.index:
        #    if year in df_bSheet.columns:
        #        cashFromOperatingActivity  = (df_bSheet.at['Total Assets', year])
        #        ee += float(cashFromOperatingActivity)
        #    else:
        #        ee += 0.0
        #else:
        #    ee += 0.0

        if 'Share Capital -' in df_bSheet.index:
            if year in df_bSheet.columns:
                cashFromOperatingActivity  = (df_bSheet.at['Share Capital -', year])
                ee += float(cashFromOperatingActivity)
            else:
                ee += 0.0
        else:
            ee += 0.0
        if 'Reserves' in df_bSheet.index:
            if year in df_bSheet.columns:
                cashFromOperatingActivity  = (df_bSheet.at['Reserves', year])
                ee += float(cashFromOperatingActivity)
            else:
                ee += 0.0
        else:
            ee += 0.0
        #if 'Borrowings' in df_bSheet.index:
        #    if year in df_bSheet.columns:
        #        cashFromOperatingActivity  = (df_bSheet.at['Borrowings', year])
        #        ee -= float(cashFromOperatingActivity)
        #    else:
        #        ee -= 0.0
        #else:
        #    ee -= 0.0
        #if 'Other Liabilities -' in df_bSheet.index:
        #    if year in df_bSheet.columns:
        #        cashFromOperatingActivity  = (df_bSheet.at['Other Liabilities -', year])
        #        ee -= float(cashFromOperatingActivity)
        #    else:
        #        ee -= 0.0
        #else:
        #    ee -= 0.0

        equity.append(ee)

    #print(roce,'% ')
    #print(equity)
    #print(sales)
    #print(eps)
    #print(cash_from_operations)

    equity_pct = []
    sales_pct = []
    eps_pct = []
    cash_pct = []

    NumYears = [1]
    if number_of_years_avail > 3:
        NumYears.append(3)
    if number_of_years_avail > 5:
        NumYears.append(5)
    if number_of_years_avail > 10:
        NumYears.append(10)

    #print(NumYears)

    for i in NumYears:
        equity_pct.append(findGrowthPct(equity[0], equity[i], i))
        sales_pct.append(findGrowthPct(sales[0], sales[i], i))
        eps_pct.append(findGrowthPct(eps[0], eps[i], i))
        cash_pct.append(findGrowthPct(cash_from_operations[0], cash_from_operations[i], i))

    #print(NumYears)
    #print(equity_pct)
    #print(sales_pct)
    #print(eps_pct)
    #print(cash_pct)

    a = ['Equity %']
    a.extend(equity_pct)
    b = ['Sales %']
    b.extend(sales_pct)
    c = ['EPS %']
    c.extend(eps_pct)
    d = ['Cash %']
    d.extend(cash_pct)

    #print(a)


    data = [ a, b, c, d]

    #print(data)
    x = [ 'Ratios ']
    x.extend(NumYears)
    #print(x)
    df  = pd.DataFrame(data, columns = x)
    #df  = pd.DataFrame(data)
    print('-----------------------------------------------------------------------------')
    print(df)
    print('-----------------------------------------------------------------------------\n\n')

    current_eps = eps[0]
    #print(current_eps)
    eps_growth  = equity_pct[-1]#min(max(5,equity_pct[-1]), sum(equity_pct)/len(equity_pct))
    #print(eps_growth)
    future_eps = current_eps*pow( (1+eps_growth/100),10)
    #print(future_eps)
    future_pe = 2*eps_pct[-1]
    #print(future_pe)
    future_price = future_eps * future_pe
    #print(future_price)
    sticker_price = future_price/pow(1.15, 10)
    #print(sticker_price)





    return sticker_price, price


import math
def findGrowthPct(fwd, base, term):
    if base <= 0.0:
        base  = 1
    if fwd <= 0.0:
        fwd = 1
    a = (math.log10(fwd) - math.log10(base))/term
    b = (pow(10, a) - 1.0)*100.0
    return b



import sys, getopt

def my_main(argv):
    filename = sys.argv[-1]
    try:
        opts, args = getopt.getopt(argv,"$hvslS:f:")
    except getopt.GetoptError:
        print( 'findStickerPrice.py -h -v  -s -S SCRIP [-f <file> -l ]')
        sys.exit(2)

    sym = 'IEX'
    stand = False
    verb = False
    check = False
    filename = 'File'

    for opt, arg in opts:
        if opt == '-h':
            print( 'findStickerPrice.py -h -v  -s -S SCRIP [ -f <filename> -l ]')
            #print ('stocksLessThanInstrinsicValue.py -h -l -m -s -$ -S <sales%> -R <ret%>')
            sys.exit()
        elif opt in ("-s"):
            stand = True
        elif opt in ("-v"):
            verb = True
        elif opt in ("-l"):
            check = True
        elif opt in ("-S"):
            sym = str(arg)
        elif opt in ("-f"):
            filename = str(arg)


    if filename == 'File' :

        intrinsic_price, price = findStickerPrice(stock=sym,standalone=stand,verbose=verb)
        print(' Symbol : ' + sym)
        print(' Sticker price of ' + sym + ' is : ' + str(intrinsic_price) )
        print(' CMP of ' + sym + ' is : ' + str(price) )

    else:
        f = open(filename)
        for sym in f:
            sym = sym.rstrip('\n')
            print(' Symbol : ' + sym)

            try:
                intrinsic_price, price = findStickerPrice(stock=sym,standalone=stand,verbose=verb)
                if(intrinsic_price == 0.0):
                    intrinsic_price, price = findStickerPrice(stock=sym,standalone=True,verbose=verb)
            except:
                print("Whew!", sys.exc_info()[0], "occurred.")
                continue

            #print(check == True)
            #print(int(price) < int(intrinsic_price))
            #print(int(intrinsic_price) > 0)
            #print((check == True) and (int(price) < int(intrinsic_price)) and (int(intrinsic_price) > 0))

            condition =  (int(price) < int(intrinsic_price)) and (int(intrinsic_price) > 0)

            #if ((check == True) and (int(price) < int(intrinsic_price)) and (int(intrinsic_price) > 0)):
            if check == True:
                if condition == True:
                    print('------------------------------------------------------------')
                    print(' Symbol : ' + sym)
                    print(' Sticker price of ' + sym + ' is : ' + str(intrinsic_price) )
                    print(' CMP of ' + sym + ' is : ' + str(price) +'\n')

            else:
                print('------------------------------------------------------------')
                print(' Symbol : ' + sym)
                print(' Sticker price of ' + sym + ' is : ' + str(intrinsic_price) )
                print(' CMP of ' + sym + ' is : ' + str(price) +'\n')




if __name__ == '__main__':
    my_main(sys.argv[1:])

