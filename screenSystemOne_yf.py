import pandas as pd
from nsepy import get_history
from datetime import date
from datetime import *; from dateutil.relativedelta import *
import calendar
import pprint

import argparse
import sys
import getopt

from getAllTheLargeCapStocks import getAllCapStocks
from getWeeklyMA_yf import getWMAandRSI


from nsetools import Nse  # Nse Driver
from pprint import pprint # just for neatness of display
import pandas as pd
import numpy as np
from yahoo_fin import stock_info as si



import yfinance as yf

def my_main(argv):
    filename = sys.argv[-1]
    try:
        opts, args = getopt.getopt(argv,"$hmsS:")
    except getopt.GetoptError:
        print( 'screenSystemOne_yf.py -h -S SCRIP [-m ] [-s]')
        sys.exit(2)




    nse = Nse()
    [   dictLargeCap, dictMidCap, dictSmallCap] =  getAllCapStocks(False)

    d  = dictLargeCap
    for opt, arg in opts:
        if opt == '-h':
            print( 'screenSystemOne_yf.py -h -S SCRIP [-m ] [-s]')
            sys.exit()
        elif opt in ("-m"):
            d = dictMidCap
        elif opt in ("-s"):
            d = dictSmallCap
        elif opt in ("-S"):
            sym = str(arg)
            wma, rsi, cmp, trnd  = getWMAandRSI(sym)
            #print(wma, rsi, cmp, trnd)
            stock = yf.Ticker(sym+".NS")
            # get all stock info
            info = stock.info
            print("--------------------------------------------------------------------------------------")
            print("                                Screener Portfolio                                    ")
            print("--------------------------------------------------------------------------------------")
            print("%4s %15s %5s %8s %8s %8s %8s %8s %8s %8s  %8s"%("No","Symbol", "Trnd", "20WMA", "     RSI(14)", "CMP", "  52WeekHigh", "  %UpPotential", "%RiskMargin","TargetPrice","%UpTarget"))
            if 'targetMedianPrice' in info.keys():
                tar = info['targetMedianPrice']
            else:
                tar = info['previousClose']
            h52 = info['fiftyTwoWeekHigh']
            upp = ((h52-cmp)/(cmp))*100.00
            tpp = ((tar-cmp)/(cmp))*100.00
            risk = ((cmp-wma)/cmp)*100.00
            print("%4s %15s %5s %10.2f %10.2f %10.2f %10.2f %10.2f %10.2f %10.2f %10.2f"%(1, sym, trnd, wma, rsi, cmp, h52, upp, risk, tar, tpp))
            sys.exit()




    #print("Venu1")
    #sym = 'GATI'
    #wma, rsi, cmp, trnd  = getWMAandRSI(sym)
    #print(wma, rsi, cmp, trnd)
    #q = si.get_live_price(sym+".NS")
    #print(q)
    #print("Venu2")


    cnt = 1
    print("--------------------------------------------------------------------------------------")
    print("                      Screener Portfolio - Weekly Data                                ")
    print("--------------------------------------------------------------------------------------")
    print("%4s %15s %5s %8s %8s %8s %8s %8s %8s %8s"%("No","Symbol", "Trnd", "20WMA", "     RSI(14)", "CMP", "  52WeekHigh", "  %UpPotential", "%RiskMargin","TargetPrice"))

    df = pd.DataFrame(columns=("No","Symbol", "Trend", "20WMA", "RSI(14)", "CMP", "52WeekHigh", "%UpPotential", "%RiskMargin", "TargetPrice", "%UpTarget"))
    for sym in d:

        #print("Venu")
        #print(sym)
        #if sym == 'ABB':
        #    continue
        try:
            wma, rsi, cmp, trnd  = getWMAandRSI(sym)
            #print(wma, rsi, cmp, trnd)  #  = 0.0, 0.0, 0.0, 'UP'
            #wma, rsi, cmp, trnd  = 0.0, 0.0, 0.0, 'UP'
            if(rsi >59.9 and rsi < 65):
            #if(rsi > -1.0 ):
                #print(sym)
                #q = nse.get_quote(sym)
                #q = si.get_live_price(sym+".NS")
                #print(q)
                stock = yf.Ticker(sym+".NS")
                # get all stock info
                info = stock.info

                #tar = info['targetMedianPrice']
                if 'targetMedianPrice' in info.keys():
                    tar = info['targetMedianPrice']
                else:
                    tar = info['currentPrice']
                h52 = info['fiftyTwoWeekHigh']
                upp = ((h52-cmp)/(cmp))*100.00
                tpp = ((tar-cmp)/(cmp))*100.00
                risk = ((cmp-wma)/cmp)*100.00
                print("%4s %15s %5s %10.2f %10.2f %10.2f %10.2f %10.2f %10.2f %10.2f"%(cnt, sym, trnd, wma, rsi, cmp, h52, upp, risk, tar))
                i = cnt -1
                df.loc[cnt] = [cnt, sym, trnd, wma, rsi, cmp, h52, upp, risk, tar, tpp]
                cnt += 1
        except:
            print(sym+" -- no data on Website")
    print("--------------------------------------------------------------------------------------")

    df = df.sort_values(by='RSI(14)', ascending=False, na_position='first')
    pprint(df)





if __name__ == '__main__':
    my_main(sys.argv[1:])
