# Import yfinance and matplotlib
import yfinance as yf

sym = "INFY"
stock = yf.Ticker(sym+".NS")
info = stock.info
print(info)

#exit



