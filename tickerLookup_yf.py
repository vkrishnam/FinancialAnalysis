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

import sys, getopt
from nsetools import Nse  # Nse Driver
from pprint import pprint # just for neatness of display
import pandas as pd
import numpy as np
from yahoo_fin import stock_info as si
from bsedata.bse import BSE

def my_main(argv):
    filename = sys.argv[-1]

    try:
        opts, args = getopt.getopt(argv,"$msS:")
    except getopt.GetoptError:
        print( 'tickerLookup_yf.py [-m  -s] -S SCRIP ')
        sys.exit(2)

    nse = Nse()
    [   dictLargeCap, dictMidCap, dictSmallCap] =  getAllCapStocks(False)

    d  = dictLargeCap
    for opt, arg in opts:
        if opt == '-h':
            #print( 'findStickerPrice.py -h -v  -s -S SCRIP [ -f <filename> -l ]')
            print( 'tickerLookup_yf.py [-m  -s] -S SCRIP ')
            sys.exit()
        elif opt in ("-s"):
            d = dictSmallCap
        elif opt in ("-m"):
            d = dictMidCap
        elif opt in ("-S"):
            string = str(arg)

    if not("string" in locals()):
        print("Please provide a string to lookup the ticker!!!")
        print( 'findStickerPrice.py -h -v  -s -S SCRIP [ -f <filename> -l ]')
        sys.exit()


    dd = [ dictLargeCap, dictMidCap, dictSmallCap]

    print("Searching to find a match for the Company name in NSE .... \n")
    matchFound = False
    for d in dd:
        for sym in d:
            fullname = d[sym][0]
            if fullname != None and string.upper() in fullname.upper():
                matchFound = True
                print(sym," -- ", d[sym][0])
                print("--------------------------------------------------------------------------------------")
    if matchFound is False:
        print(" NO MATCH FOUND in NSE !!!! ")
        print("Searching to find a match for the Company name in BSE .... \n")
        #b = BSE()
        b = BSE(update_codes = True)
        d = b.getScripCodes()
        for scrip_code in d:
            fullname = d[scrip_code]
            if fullname != None and string.upper() in fullname.upper():
                matchFound = True
                print(scrip_code," -- ", d[scrip_code])
                print("--------------------------------------------------------------------------------------")


    if matchFound is False:
        print(" NO MATCH FOUND in BSE !!!! ")






if __name__ == '__main__':
    my_main(sys.argv[1:])
