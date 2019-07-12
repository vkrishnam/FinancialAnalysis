#############################################
## https://www.quandl.com/data/TC1-Indian-Equities-Adjusted-End-of-Day-Prices/usage/quickstart/python
#############################################


import quandl
quandl.ApiConfig.api_key = "1Rw_ovhmRsBYyzx4p3cL"
#mydata = quandl.get("FRED/GDP")
mydata = quandl.get("DEB/INFY_A_PE")
print(mydata)
#data = quandl.get_table('ZACKS/FC', paginate=True)
#print(data.keys())
