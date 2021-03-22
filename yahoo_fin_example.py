#  import stock_info module from yahoo_fin
from yahoo_fin import stock_info as si

# get live price of Apple
aapl = si.get_live_price("aapl")


infy = si.get_live_price("infy.ns")

print(" AAPL : " , aapl)
print(" INFY : " , infy)
