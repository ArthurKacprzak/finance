import fxcmpy
import time
import datetime as dt
from pyti.relative_strength_index import relative_strength_index as rsi


###### USER PARAMETERS ######
#phiphi
#token = "1a7dd8a06ab9e998d650cb750f2bd039860af8c2"
#moi
token = '52f024b13ae656b23cdbf7af83b784fece1827f8'
symbols = ['EUR/USD', 'GBP/USD', 'EUR/JPY', 'USD/JPY', 'CHF/JPY']
timeframe = "m1"
rsi_periods = 14
upper_rsi = 70.0
lower_rsi = 30.0
amount = 1
stop = -10
limit = 10
#############################

openSymbols = []

def position(is_buy, d):
    print("Opening a position")
    opentrade = con.open_trade(symbol=d, is_buy=is_buy,
                            amount=amount, time_in_force='GTC',
                            order_type='AtMarket', is_in_pips=True,
                            limit=limit, stop=stop)




def getLastRsiValue(devise):
    data = con.get_candles(devise, period=timeframe, number=200)
    rsiList = rsi(data['bidclose'], rsi_periods)
    return rsiList[-1];


def checkIfClosedPosition():
    #ind indicates whether the symbol has still an open position or not. 1 for yes and 0 for no.
    ind = 0
    #retrieve open positions
    openpositions = con.get_open_positions(kind='list')
    for symbol in openSymbols:
        for position in openpositions:
            if (position['currency'] == symbol):
                ind = 1
        #symbol does not have a current open position
        if (ind == 0):
            openSymbols.remove(symbol)
            symbols.append(symbol)
        #reste indicator
        else:
            ind = 0



con = fxcmpy.fxcmpy(access_token=token, log_level='error', server='demo', log_file='log.txt')

while (True):
    print(openSymbols)
    print(symbols)
    checkIfClosedPosition()
    for symbol in symbols:
        rsiValue = getLastRsiValue(symbol)

        print(symbol + " RSI : " + str(rsiValue))

        if (rsiValue > upper_rsi):
            position(False, symbol) # Sell
            openSymbols.append(symbol)
            symbols.remove(symbol)
            #con.close()
            #exit(1)
        if (rsiValue < lower_rsi):
            position(True, symbol) # Buy
            openSymbols.append(symbol)
            symbols.remove(symbol)
            #con.close()
            #exit(1)
    time.sleep(5)
    print("----------------");

con.close()
