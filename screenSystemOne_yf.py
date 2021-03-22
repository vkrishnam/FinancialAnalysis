import pandas as pd
from nsepy import get_history
from datetime import date
from datetime import *; from dateutil.relativedelta import *
import calendar
import pprint

import argparse
import sys

from getAllTheLargeCapStocks import getAllCapStocks
from getWeeklyMA_yf import getWMAandRSI


from nsetools import Nse  # Nse Driver
from pprint import pprint # just for neatness of display
import pandas as pd
import numpy as np


def my_main():
    option = sys.argv[-1]

    nse = Nse()
    [   dictLargeCap, dictMidCap, dictSmallCap] =  getAllCapStocks(False)

    d  = dictLargeCap
    #d = { 'INFY' : 123}

    if (option == '-m'):
        d = dictMidCap
    if (option == '-s'):
        d = dictSmallCap



    cnt = 1
    print("--------------------------------------------------------------------------------------")
    print("                      Screener Portfolio - Weekly Data                                ")
    print("--------------------------------------------------------------------------------------")
    print("%4s %15s %5s %8s %8s %8s %8s %8s %8s"%("No","Symbol", "Trnd", "20WMA", "     RSI(14)", "CMP", "  52WeekHigh", "  %UpPotential", "%RiskMargin"))

    df = pd.DataFrame(columns=("No","Symbol", "Trend", "20WMA", "RSI(14)", "CMP", "52WeekHigh", "%UpPotential", "%RiskMargin"))
    for sym in d:
        #print(sym)
        #if sym == 'ADANIGAS':
        #    continue
        wma, rsi, cmp, trnd  = getWMAandRSI(sym)
        #print(wma, rsi, cmp, trnd)  #  = 0.0, 0.0, 0.0, 'UP'
        #wma, rsi, cmp, trnd  = 0.0, 0.0, 0.0, 'UP'
        if(rsi >59.9 and rsi < 65):
        #if(rsi > -1.0 ):
            q = nse.get_quote(sym)
            h52 = q['high52']
            upp = ((h52-cmp)/(cmp))*100.00
            risk = ((cmp-wma)/cmp)*100.00
            print("%4s %15s %5s %10.2f %10.2f %10.2f %10.2f %10.2f %10.2f"%(cnt, sym, trnd, wma, rsi, cmp, h52, upp, risk))
            i = cnt -1
            df.loc[cnt] = [cnt, sym, trnd, wma, rsi, cmp, h52, upp, risk]
            cnt += 1
    print("--------------------------------------------------------------------------------------")

    df = df.sort_values(by='RSI(14)', ascending=False, na_position='first')
    pprint(df)





if __name__ == '__main__':
    my_main()
