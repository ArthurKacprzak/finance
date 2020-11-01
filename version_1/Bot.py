import fxcmpy
import socketio
import sys
import time
import datetime as dt
from pyti.relative_strength_index import relative_strength_index as rsi
from pyti.simple_moving_average import simple_moving_average as sma
from pyti.moving_average_convergence_divergence import moving_average_convergence_divergence as macd
from pyti.exponential_moving_average import exponential_moving_average as ema

###### USER PARAMETERS ######
#phiphi
token = "1a7dd8a06ab9e998d650cb750f2bd039860af8c2"
#moi
#token = '52f024b13ae656b23cdbf7af83b784fece1827f8'
symbols = ['EUR/USD', 'GBP/USD', 'AUD/USD']
bTValues = []
buyposition = 0
sellposition = 0
ind = 0
#############################

openSymbols = []

def position(is_buy, d, amount, limit, stop):
    print("Opening a position")
    opentrade = con.open_trade(symbol=d, is_buy=is_buy,
                            amount=amount, time_in_force='GTC',
                            order_type='AtMarket', is_in_pips=False,
                            limit=limit, stop=stop)

def checkIfClosedPosition():
    #ind indicates whether the symbol has still an open position or not. 1 for yes and 0 for no.
    ind = 0
    #retrieve open positions
    openpositions = con.get_open_positions(kind='list')
    for position in openpositions:
        if (position['currency'] == 'EUR/USD'):
            ind = 1
    return ind

def checkemaCross(emaInd, slowemaList, fastemaList, stockslowEma, stockfastEma):

    if (stockfastEma < stockslowEma and fastemaList[-1] > slowemaList[-1]):
        emaInd = 1
    if (stockfastEma > stockslowEma and fastemaList[-1] < slowemaList[-1]):
        emaInd = 0
    return emaInd

def backTesting():

    global ind
    balance = 50000
    global sellposition
    global buyposition
    stockfastEma = 0
    stockslowEma = 0
    emaInd = 0
    sDay = int(input("Enter backtesting initial day as [DD] :"))
    sMonth = int(input("Enter backtesting initial month as [MM] :"))
    sYear = int(input("Enter backtesting initial year as [YYYY] :"))
    sDate = dt.datetime(sYear, sMonth, sDay)
    eDay = int(input("Enter backtesting ending day as [DD] :"))
    eMonth = int(input("Enter backtesting ending month as [MM] :"))
    eYear = int(input("Enter backtesting ending year as [YYYY] :"))
    eDate = dt.datetime(eYear, eMonth, eDay)

    for symbol in symbols:
        ind = 0
        emaInd = 0
        stockfastEma = 0
        stockslowEma = 0
        buyposition = 0
        sellposition = 0
        bTValues = con.get_candles(symbol, period="H1", start=sDate, end=eDate, columns=['date', 'bidclose', 'askclose'], with_index=False)

        while (ind < len(bTValues)):
            #retrieving candles
            smaData = con.get_candles(symbol, period="H1", end=bTValues['date'][ind], number=110)
            slowemaData = con.get_candles(symbol, period="H1", end=bTValues['date'][ind], number=26)
            fastemaData = con.get_candles(symbol, period="H1", end=bTValues['date'][ind], number=9)

            #calculating indicators
            smaList = sma(smaData['bidclose'], 110)
            slowemaList = ema(slowemaData['bidclose'], 26)
            fastemaList = ema(fastemaData['bidclose'], 9)

            if (stockfastEma == 0 and stockslowEma == 0):
                stockfastEma = fastemaList[-1]
                stockslowEma = slowemaList[-1]

            #checking if indicators cross (trends)
            emaInd = checkemaCross(emaInd, slowemaList, fastemaList, stockslowEma, stockfastEma)

            #long conditions
            if (buyposition == 0 and emaInd == 1 and bTValues['bidclose'][ind] > smaList[-1]):
                print("You opened a buy position on " + str(bTValues['date'][ind]))
                print()
                buyposition = bTValues['bidclose'][ind]

            #short conditions
            if (sellposition == 0 and bTValues['bidclose'][ind] < smaList[-1] and emaInd == 0):
                print("You opened a sell position on " + str(bTValues['date'][ind]))
                print()
                sellposition = bTValues['bidclose'][ind]

            stockfastEma = fastemaList[-1]
            stockslowEma = slowemaList[-1]

            #profit or loss conditions + balance update
            if (buyposition != 0 and bTValues['bidclose'][ind] < buyposition - (buyposition/10000) * 70):
                buyposition = 0
                balance = balance - (((balance/10000) * 70))
                print("You lost money!")
                print("New balance : " + str(balance))
                print()
            if (buyposition != 0 and bTValues['bidclose'][ind] >= buyposition + (buyposition/100)*16/10):
                buyposition = 0
                balance = balance + (((balance/100)*16/10))
                print("You won money!")
                print("New balance : " + str(balance))
                print()
            if (sellposition != 0 and bTValues['bidclose'][ind] > sellposition + (sellposition/10000) * 70):
                sellposition = 0
                balance = balance - (((balance/10000) * 70))
                print("You lost money!")
                print("New balance : " + str(balance))
                print()
            if (sellposition != 0 and bTValues['bidclose'][ind] < sellposition - (sellposition/100)*16/10):
                sellposition = 0
                balance = balance + (((balance/100)*16/10))
                print("You won money!")
                print("New balance : " + str(balance))
                print()
            ind+=1


def liveApp():
    
    emaInd = 0
    stockfastEma = 0
    stockslowEma = 0
    liveValue = 0
    limit = 0
    stop = 0
    symbol = 'EUR/USD'
    
    while (True):
        pos = checkIfClosedPosition()
        #retrieving candles
        liveValue = con.get_candles(symbol, period="H1", columns=['date', 'bidclose', 'askclose'], with_index=False, number=1)
        smaData = con.get_candles(symbol, period="H1", number=110)
        slowemaData = con.get_candles(symbol, period="H1", number=26)
        fastemaData = con.get_candles(symbol, period="H1", number=9)

        #calculating indicators
        smaList = sma(smaData['bidclose'], 110)
        slowemaList = ema(slowemaData['bidclose'], 26)
        fastemaList = ema(fastemaData['bidclose'], 9)

        if (stockfastEma == 0 and stockslowEma == 0):
            stockfastEma = fastemaList[-1]
            stockslowEma = slowemaList[-1]

        #checking if indicators cross (trends)
        emaInd = checkemaCross(emaInd, slowemaList, fastemaList, stockslowEma, stockfastEma)

        if (pos == 0 and emaInd == 1 and liveValue['bidclose'][0] > smaList[-1]):
            #Calculation of our profit gain / stop loss percentage based on live value
            limit = liveValue['bidclose'][0] + (liveValue['bidclose'][0]/100)*16/10/2
            stop = liveValue['bidclose'][0] - (liveValue['bidclose'][0]/10000)*70/2
            #Buy Position
            position(True, symbol, 1000, limit, stop)
        if (pos == 0 and liveValue['bidclose'][0] < smaList[-1] and emaInd == 0):
            #Calculation of our profit gain / stop loss percentage based on live value
            limit = liveValue['bidclose'][0] - (liveValue['bidclose'][0]/100)*16/10/2
            stop = liveValue['bidclose'][0] + (liveValue['bidclose'][0]/10000)*70/2
            # Sell position 
            position(False, symbol, 1000, limit, stop)

#Connection to fxcm api
con = fxcmpy.fxcmpy(access_token=token, log_level='error', server='demo', log_file='log.txt')

if (len(sys.argv) > 1 and sys.argv[1].lower() == '-b'):
    backTesting()
else:
    liveApp()

#closing connection to fxcm api
con.close()
