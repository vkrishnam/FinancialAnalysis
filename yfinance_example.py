# Import yfinance and matplotlib
import yfinance as yf

#sym = 'INFRATEL.NS'
sym = 'INFY.NS'

# Get the data for the SPY ETF by specifying the stock ticker, start date, and end date
try:
    data = yf.download( sym,'2021-03-01','2021-03-09', progress=False)
    print(data)
except Exception:
    pass
    print( sym + 'is delisted !!!')


