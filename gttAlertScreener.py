
import yfinance as yf
import time
import csv
import sys
from yahoo_fin import stock_info as si
from twilio.rest import Client
from datetime import datetime


dict_alerts = {}

def my_csv(csvfilename):
    with open(csvfilename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            #print(row[0], ', ',  row[1])
            sym = row[0] + '.NS'
            SLP = float(row[1].replace(',', ''))
            live_price = si.get_live_price(sym)
            if(live_price < SLP):
                booody = "ALERT !!! "+ row[0] +" stock price got lower than SLP !!!"
                if(dict_alerts.get(sym) is None):
                    dict_alerts[sym] = live_price
                    client = Client("AC9f438ba67912243c507e5b5310dbc846", "223fb1602b51981b52378c900d95974f")
                    client.messages.create(to="+919880627826", from_="+14243733536", body=booody)
                print(booody)




def my_main2():

    while True:
        time.sleep(5)
        print(" Hello GTT Alerts !!! ")


def my_main():
    filename = sys.argv[-1]
    if (filename == 'gttAlertScreener.py'):
        print(" Hello GTT Alerts !!! ")
        pass
    else:
        while True:
            now = datetime.now()
            s2 = now.strftime("%d/%m/%Y, %H:%M:%S")
            print("->  ", s2) #time.time())
            my_csv(filename)
            time.sleep(30)






if __name__ == '__main__':
    my_main()
