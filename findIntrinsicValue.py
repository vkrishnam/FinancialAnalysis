
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
import math
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

import math
def findGrowthPct(fwd, base, term):
    if base <= 0.0:
        base  = 1
    if fwd <= 0.0:
        fwd = 1
    a = (math.log10(fwd) - math.log10(base))/term
    b = (pow(10, a) - 1.0)*100.0
    return b


from yahoo_fin import stock_info as si
from bsedata.bse import BSE
import datetime

def findIntrinsicValue(stock = 'IEX', standalone = False,verbose=True, aggresive=False):
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
    print(" ROCE   : ", roce)
    roe = findROE(page_content, stock)
    #print("\nROE  : ", roe)
    pe = findPE(page_content, stock)
    print(" PE     : ", pe)
    dy = findDividendYield(page_content, stock)
    print(" Dividend Yield  : ", dy)

    #f = open("filecontent.html", 'w')
    #f.write(str(page_content));
    #f.close()
    #print('Debug:::: '+str(stock)+'.NS')

    if stock.isdigit():
        b = BSE(update_codes = True)
        q = b.getQuote(stock)
        price = q["currentValue"]
    else:
        price = si.get_live_price(str(stock)+'.NS')

    discount_rate = 9
    first_five = 15
    next_five = 10
    terminal = 5
    term = 10
    num_years_data = 5
    current_year  = 2023
    today = datetime.date.today()
    current_year = today.year

    cash_from_operations = []
    capex = []
    free_cash_flow = []

    df_cash_flow = getCashFlowStatement(page_content,verbose)
    df_PandL = getPandLStatement(page_content,verbose)
    df_bSheet = getBalanceSheetStatement(page_content,verbose)

    months = ['Mar ', 'Dec ']
    #year  = current_year
    year = 'Mar '+str(current_year)
    fixed_month = 'Mar '
    found_match = False

    for month in months:
        year1 = month + str(current_year)
        year2 = month + str(current_year-1)
        if year1 in df_cash_flow.columns:
            fixed_month = month
            found_match = True
            year = year1
            break;
        if year2 in df_cash_flow.columns:
            fixed_month = month
            found_match = True
            year = year2
            break;
    if found_match == False:
        return 0.0, 0.0

    if verbose:
        print('Symbol : ' + symbol)
    total_debt = float(df_bSheet.at['Borrowings +', year])
    share_capital = float(df_bSheet.at['Share Capital -', year])
    cash_cash_balance = float(df_bSheet.at['Cash Equivalents', year])

    future_cash_flow = []
    future_disc_cash_flow = []

    for i in range(num_years_data):
        year  = current_year - i
        year =  fixed_month +str(year)

        if 'Cash from Operating Activity -' in df_cash_flow.index:
            if year in df_cash_flow.columns:
                cashFromOperatingActivity  = (df_cash_flow.at['Cash from Operating Activity -', year])
            else:
                continue
        else:
            continue

        cashFromOperatingActivity = float(cashFromOperatingActivity)
        cash_from_operations.append(cashFromOperatingActivity)

        investment_made = 0.0
        #if 'Investments purchased' in df_cash_flow.index:
        #    if year in df_cash_flow.columns:
        #        investment_made  = float(df_cash_flow.at['Investments purchased', year])
        if 'Fixed assets purchased' in df_cash_flow.index:
            if year in df_cash_flow.columns:
                investment_made  += float(df_cash_flow.at['Fixed assets purchased', year])


        investment_made = float(investment_made)
        capex.append(investment_made)

        fcf = cashFromOperatingActivity + investment_made
        free_cash_flow.append(fcf)



        #print( year +'  ' , fcf)

    if len(free_cash_flow) == 0:
        return 0.0, price

    average_fcf = sum(free_cash_flow)/len(free_cash_flow)

    if aggresive is True:
        average_fcf = free_cash_flow[0]
        pct = findGrowthPct(free_cash_flow[0], free_cash_flow[-1], len(free_cash_flow)-1)
        if pct < 14:
            pct = 14
        first_five = pct
        next_five = pct
        discount_rate = 8

        #print(free_cash_flow)
        #print('base fcf : ' + str(free_cash_flow[-1]))
        #print('fwd fcf : ' + str(free_cash_flow[0]))
        #print('term : ' + str(len(free_cash_flow)-1))

        print('percentage : '+str(pct))




    #print('Average FCF : ' + str(average_fcf))

    for i in range(term):
        if i < 5:
            future_fcf = average_fcf*(1+float(first_five)/100)
            disc_future_fcf = future_fcf/pow((1+float(discount_rate)/100), i+1)
        else:
            future_fcf = average_fcf*(1+float(next_five)/100)
            disc_future_fcf = future_fcf/pow((1+float(discount_rate)/100), i+1)

        future_cash_flow.append(future_fcf)
        future_disc_cash_flow.append(disc_future_fcf)

        average_fcf = future_fcf

        #print( str(i) + ' ' +str(future_fcf) + ' ' + str(disc_future_fcf))


    terminal_value = future_cash_flow[-1] * (1+float(terminal)/100) / ((float(discount_rate)-float(terminal))/100)
    #print("Terminal Value : "+str(terminal_value))
    pv_terminal_value = terminal_value/pow(1+float(discount_rate)/100, term)
    #print("PV Terminal Value : "+str(pv_terminal_value))

    total_pv_of_cash_flow = sum(future_disc_cash_flow) + pv_terminal_value
    #print("Total PV of Cash FLow : "+str(total_pv_of_cash_flow))

    net_debt = -1*total_debt + cash_cash_balance
    num_of_shares = share_capital * pow(10, 7) / float(face)

    #print('Num shares : '+ str(num_of_shares))

    if num_of_shares == 0:
        intrinsic_price = 0.0
    else:
        intrinsic_price = (total_pv_of_cash_flow + net_debt) * pow(10, 7) / num_of_shares

    #print('Intrinsic Value : ' + str(intrinsic_price) )



    return intrinsic_price, price


import sys, getopt

def my_main(argv):
    filename = sys.argv[-1]
    try:
        opts, args = getopt.getopt(argv,"$havslS:f:")
    except getopt.GetoptError:
        print( 'findIntrinsicValue.py -h -a -v -l -s -S SCRIP [-f <file> ]')
        sys.exit(2)

    sym = 'IEX'
    stand = False
    verb = False
    check = False
    filename = 'File'
    aggres = False

    for opt, arg in opts:
        if opt == '-h':
            print( 'findIntrinsicValue.py -h -a -v -l  -s -S SCRIP [ -f <filename> ]')
            #print ('stocksLessThanInstrinsicValue.py -h -l -m -s -$ -S <sales%> -R <ret%>')
            sys.exit()
        elif opt in ("-a"):
            aggres = True
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
        sym = sym.rstrip('\n')

        print(' Symbol :  ' + sym)
        intrinsic_price, price = findIntrinsicValue(stock=sym,standalone=stand,verbose=verb,aggresive=aggres)
        print(" Intrinsic Value is   : %5d " % ( (math.trunc(intrinsic_price))) )
        print(" Curr Market Price is : %5d " % ( (math.trunc(price))) )

    else:
        f = open(filename)
        for sym in f:
            sym = sym.rstrip('\n')
            print(' Symbol : ' + sym)

            try:
                intrinsic_price, price = findIntrinsicValue(stock=sym,standalone=stand,verbose=verb)
                if(intrinsic_price == 0.0):
                    intrinsic_price, price = findIntrinsicValue(stock=sym,standalone=True,verbose=verb)
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
                    print(' Intrinsic Value of ' + sym + ' is : ' + str(math.trunc(intrinsic_price)) )
                    print(' CMP of ' + sym + ' is : ' + str(math.trunc(price)) +'\n')

            else:
                print('------------------------------------------------------------')
                print(' Symbol : ' + sym)
                print(' Intrinsic Value of ' + sym + ' is : ' + str(math.trunc(intrinsic_price)) )
                print(' CMP of ' + sym + ' is : ' + str(math.trunc(price)) +'\n')




if __name__ == '__main__':
    my_main(sys.argv[1:])

