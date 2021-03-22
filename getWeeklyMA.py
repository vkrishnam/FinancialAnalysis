import pandas as pd
from nsepy import get_history
from datetime import date
from datetime import *; from dateutil.relativedelta import *
import calendar
import pprint

import argparse
import sys
from nsetools import Nse  # Nse Driver



def getWMA(sym='LT', period=20):
    end = today = date.today()
    start = today+relativedelta(months=-12)
    data = get_history(symbol=sym, start=start, end=end )
    #print(sym, start, end)
    #print(data)
    if data.empty:
        wma = 0.0
        limited_wma = "{:.2f}".format(wma)
        return limited_wma

    wdata = data.drop(['Symbol', 'Series', 'Prev Close', 'Last', 'VWAP', 'Turnover', 'Trades', 'Deliverable Volume', '%Deliverble'], axis = 1)
    agg_dict = {'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'mean'}

    wdata.index = pd.to_datetime(wdata.index)
    wdata = wdata.astype(float)
    #print(wdata)
    r_df = wdata.resample('W').agg(agg_dict)
    wma = (float)(r_df.tail(period)[['Close']].mean())
    limited_wma = "{:.2f}".format(wma)
    return limited_wma


def computeRSI (data, time_window):
    if data.empty:
        rsi = 0.0
        return rsi

    diff = data.diff(1).dropna()        # diff in one field(one day)

    #this preservers dimensions off diff values
    up_chg = 0 * diff
    down_chg = 0 * diff

    # up change is equal to the positive difference, otherwise equal to zero
    up_chg[diff > 0] = diff[ diff>0 ]

    # down change is equal to negative deifference, otherwise equal to zero
    down_chg[diff < 0] = diff[ diff < 0 ]

    # check pandas documentation for ewm
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
    # values are related to exponential decay
    # we set com=time_window-1 so we get decay alpha=1/time_window
    up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()

    rs = abs(up_chg_avg/down_chg_avg)
    rsi = 100 - 100/(1+rs)
    return rsi


def getWMAandRSI(sym='LT', adj=0.0, window=20, period=14):
    end = today = date.today()
    start = today+relativedelta(months=-12)
    data = get_history(symbol=sym, start=start, end=end )
    if data.empty:
        wma = 0.0
        limited_wma = "{:.2f}".format(wma)
        rsi = (0.0)
        limited_rsi = rsi #"{:.2f}".format(rsi)

        current = (0.0)
        limited_current = current #"{:.2f}".format(current)
        return limited_wma, limited_rsi, limited_current, 'UP'

    wdata = data.drop(['Symbol', 'Series', 'Prev Close', 'Last', 'VWAP', 'Turnover', 'Trades', 'Deliverable Volume', '%Deliverble'], axis = 1)
    agg_dict = {'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'mean'}

    wdata.index = pd.to_datetime(wdata.index)
    wdata = wdata.astype(float)
    r_df = wdata.resample('W').agg(agg_dict)
    wma = (float)(r_df.tail(window)[['Close']].mean())
    limited_wma = wma + (adj/100.0)*wma #"{:.2f}".format(wma)

    r_df['RSI'] = computeRSI(r_df['Close'], period)
    rsi = (float)(r_df.tail(1)[['RSI']].mean())
    limited_rsi = rsi #"{:.2f}".format(rsi)


    #if( len( r_df[:-3]['Close']) < 14):
    #    rsi = 0.0
    #else:
    #    rsi  = computeRSI(r_df[:-3]['Close'], period).tail(1).mean()
    rsi  = computeRSI(r_df[:-3]['Close'], period).tail(1).mean()

    if ( (limited_rsi - rsi) <  0.0 ):
        trend = 'DOWN'
    else:
        trend = 'UP'


    current = (float)(wdata.tail(1)[['Close']].mean())
    limited_current = current #"{:.2f}".format(current)

    return limited_wma, limited_rsi, limited_current, trend

def getRSI(sym='LT', period=14):
    end = today = date.today()
    start = today+relativedelta(months=-12)
    data = get_history(symbol=sym, start=start, end=end )
    wdata = data.drop(['Symbol', 'Series', 'Prev Close', 'Last', 'VWAP', 'Turnover', 'Trades', 'Deliverable Volume', '%Deliverble'], axis = 1)
    agg_dict = {'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'mean'}

    wdata.index = pd.to_datetime(wdata.index)
    wdata = wdata.astype(float)
    r_df = wdata.resample('W').agg(agg_dict)
    r_df['RSI'] = computeRSI(r_df['Close'], period)
    rsi = (float)(r_df.tail(1)[['RSI']].mean())
    limited_rsi = "{:.2f}".format(rsi)
    return limited_rsi


def my_main():
    filename = sys.argv[-1]
    nse = Nse()

    sym = 'INFY'

    if (filename == 'getWeeklyMA.py'):
        print('Hello Python')
        print(sym +' : ' + getWMA(sym) + '\n')
        print("------------------------------------------------------------------")
        print("                       Portfolio - Weekly Data  ")
        print("------------------------------------------------------------------")
        print("%4s %15s %5s %8s %8s %8s  %8s %8s %7s"%("No","Symbol", "trend", "20WMA", "     RSI(14)", "    CMP""  52WeekHigh", "  %UpPotential", "%RiskMargin", "Ratio"))
        wma, rsi, cmp, trend = getWMAandRSI(sym, -2.0)
        #print(wma);
        q = nse.get_quote(sym)
        h52 =  q['high52']
        upp = ((h52-cmp)/(cmp))*100.00
        risk = ((cmp-wma)/cmp)*100.00
        ratio = upp/risk
        print("%4s %15s %5s %10.2f %10.2f %10.2f %10.2f %10.2f %10.2f %10.2f"%(1, sym, trend, wma, rsi, cmp, h52, upp, risk, ratio))
    else:
        # Using readlines()
        file1 = open(filename, 'r')
        Lines = file1.readlines()
        print("------------------------------------------------------------------")
        print("                       Portfolio - Weekly Data  ")
        print("------------------------------------------------------------------")
        print("%4s %15s %5s %8s %8s %8s  %8s %8s %7s"%("No","Symbol", "trend", "20WMA", "     RSI(14)", "    CMP""  52WeekHigh", "  %UpPotential", "%RiskMargin", "Ratio"))
        cnt = 1

        for line in Lines:
            sym = line.strip()
            #print("{} {} {}".format(cnt, sym, getWMA(sym)))
            #print("%4s %15s %8s %8s"%(cnt, sym, getWMA(sym), getRSI(sym)))
            wma, rsi, cmp, trend = getWMAandRSI(sym, -2.0)
            #print(wma);
            q = nse.get_quote(sym)
            h52 =  q['high52']
            upp = ((h52-cmp)/(cmp))*100.00
            risk = ((cmp-wma)/cmp)*100.00
            ratio = upp/risk
            print("%4s %15s %5s %10.2f %10.2f %10.2f %10.2f %10.2f %10.2f %10.2f"%(cnt, sym, trend, wma, rsi, cmp, h52, upp, risk, ratio))
            cnt += 1





if __name__ == '__main__':
    my_main()









