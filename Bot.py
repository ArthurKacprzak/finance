import fxcmpy
import time
import datetime as dt
from pyti.relative_strength_index import relative_strength_index as rsi


###### USER PARAMETERS ######
#phiphi
#token = "1a7dd8a06ab9e998d650cb750f2bd039860af8c2"
#moi
token = 'cb0685731aac9d8a261be8c73e16d33c33069722'
symbol = ['EUR/USD', 'GBP/USD', 'EUR/JPY', 'USD/JPY', 'CHF/JPY']
timeframe = "m1"
rsi_periods = 14
upper_rsi = 70.0
lower_rsi = 30.0
amount = 1
stop = -5
limit = 10
#############################

symbolEnter = []

def enter(is_buy, d):
    print("Open enter")
    opentrade = con.open_trade(symbol=d, is_buy=is_buy,
                            amount=amount, time_in_force='GTC',
                            order_type='AtMarket', is_in_pips=True,
                            limit=limit, stop=stop)




def getLastRsiValue(devise):
    data = con.get_candles(devise, period=timeframe, number=200)
    rsiList = rsi(data['bidclose'], rsi_periods)
    return rsiList[-1];


con = fxcmpy.fxcmpy(access_token=token, log_level='error', server='demo', log_file='log.txt')

while (True):
    for i in range(len(symbol)):
        rsiValue = getLastRsiValue(symbol[i])

        print(symbol[i] + " RSI : " + str(rsiValue))

        if (rsiValue > upper_rsi):
            enter(False, symbol[i]) # Sell
            symbolEnter.append(symbol[i])
            symbol.remove(symbol[i])
            con.close()
            exit(1)
        if (rsiValue < lower_rsi):
            enter(True, symbol[i]) # Buy
            symbolEnter.append(symbol[i])
            symbol.remove(symbol[i])
            con.close()
            exit(1)
    time.sleep(5)
    print("----------------");



con.close()


# This function closes all positions that are in the direction BuySell, "B" = Close All Buy Positions, "S" = Close All Sell Positions, uses symbol
def exit(BuySell=None):
    openpositions = con.get_open_positions(kind='list')
    isbuy = True
    if BuySell == "S":
        isbuy = False
    for position in openpositions:
        if position['currency'] == symbol:
            if BuySell is None or position['isBuy'] == isbuy:
                print("   Closing tradeID: " + position['tradeId'])
                try:
                    closetrade = con.close_trade(trade_id=position['tradeId'], amount=position['amountK'])
                except:
                    print("   Error Closing Trade.")
                else:
                    print("   Trade Closed Successfully.")
