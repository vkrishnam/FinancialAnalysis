from nsetools import Nse  # Nse Driver
from pprint import pprint # just for neatness of display


def getListOfNseStocks(verbose=False):
    nse = Nse()
    all_stock_codes = nse.get_stock_codes()
    if verbose:
        pprint(all_stock_codes)
    return all_stock_codes


def getTotalOfNseStocks(verbose=False):
    nse = Nse()
    all_stock_codes = nse.get_stock_codes()
    if verbose:
        print("Total number of stocks : ", len(all_stock_codes))
    return len(all_stock_codes)
