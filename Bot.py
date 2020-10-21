import fxcmpy
import time
import datetime as dt
from pyti.relative_strength_index import relative_strength_index as rsi
from pyti.simple_moving_average import simple_moving_average as sma
from pyti.moving_average_convergence_divergence import moving_average_convergence_divergence as macd
from pyti.exponential_moving_average import exponential_moving_average as ema


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
bTValues = []
#############################

openSymbols = []

# def rsi(data, period):

#     catch_errors.check_for_period_error(data, period)

#     period = int(period)
#     changes = [data_tup[1] - data_tup[0] for data_tup in zip(data[::1], data[1::1])]

#     filtered_gain = [val < 0 for val in changes]
#     gains = [0 if filtered_gain[idx] == True else changes[idx] for idx in range(0, len(filtered_gain))]

#     filtered_loss = [val > 0 for val in changes]
#     losses = [0 if filtered_loss[idx] == True else abs(changes[idx]) for idx in range(0, len(filtered_loss))]

#     avg_gain = np.mean(gains[:period])
#     avg_loss = np.mean(losses[:period])

#     rsi = []
#     if avg_loss == 0:
#         rsi.append(100)
#     else:
#         rs = avg_gain / avg_loss
#         rsi.append(100 - (100 / (1 + rs)))

#     for idx in range(1, len(data) - period):
#         avg_gain = ((avg_gain * (period - 1) +
#                     gains[idx + (period - 1)]) / period)
#         avg_loss = ((avg_loss * (period - 1) +
#                     losses[idx + (period - 1)]) / period)

#         if avg_loss == 0:
#             rsi.append(100)
#         else:
#             rs = avg_gain / avg_loss
#             rsi.append(100 - (100 / (1 + rs)))

#     rsi = fill_for_noncomputable_vals(data, rsi)

#     return rsi

def position(is_buy, d):
    print("Opening a position")
    opentrade = con.open_trade(symbol=d, is_buy=is_buy,
                            amount=amount, time_in_force='GTC',
                            order_type='AtMarket', is_in_pips=True,
                            limit=limit, stop=stop)




def getLastRsiValue(devise):
    data = con.get_candles(devise, period=timeframe, number=200)
    rsiList = rsi(data['bidclose'], rsi_periods)
    return rsiList[-1]


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

# def checkProfitLoss(ind, symbol, buyposition, sellposition):
#     if (sellposition != 0 and sellposition - bTValues['askclose'][ind] > 0.001):
#         profittrades += 1
#         sellposition = 0
#         print("profit made!")
#     if (sellposition != 0 and sellposition - bTValues['askclose'][ind] < 0.001):
#         sellposition = 0
#         losstrades += 1
#         print("loss made!")
#     if (buyposition != 0 and buyposition - bTValues['bidclose'][ind] < 0.001):
#         buyposition = 0
#         profittrades +=1
#         print("prodit made!")
#     if (buyposition != 0 and buyposition - bTValues['bidclose'][ind] > 0.001):
#         buyposition = 0
#         losstrades +=1
#         print("loss made!")


def backTesting():

    ind = 0
    profittrades = 0
    losstrades = 0
    sellposition = 0
    buyposition = 0
    sDay = int(input("Enter backtesting initial day as [DD] :"))
    sMonth = int(input("Enter backtesting initial month as [MM] :"))
    sYear = int(input("Enter backtesting initial year as [YYYY] :"))
    sDate = dt.datetime(sYear, sMonth, sDay)
    eDay = int(input("Enter backtesting ending day as [DD] :"))
    eMonth = int(input("Enter backtesting ending month as [MM] :"))
    eYear = int(input("Enter backtesting ending year as [YYYY] :"))
    eDate = dt.datetime(eYear, eMonth, eDay)
    bTtimeframe = input("Enter backtesting timeframe :")

    for symbol in symbols:
        ind = 0
        bTValues = con.get_candles(symbol, period=bTtimeframe, start=sDate, end=eDate, columns=['date', 'bidclose', 'askclose'], with_index=False)
        

        while (ind < len(bTValues)):
            #STRATEGY TO TEST
            rsiData = con.get_candles(symbol, period=bTtimeframe, end=bTValues['date'][ind], number=500)
            smaData = con.get_candles(symbol, period="H1", end=bTValues['date'][ind], number=111)
            emaData = con.get_candles(symbol, period="H1", end=bTValues['date'][ind], number=27)

            rsiList = rsi(rsiData['bidclose'], 14)
            smaList = sma(smaData['bidclose'], 110)

            print(rsiList[-1])
            print(smaList[-1])

        #     if (sellposition == 0 and rsiList[-1] > 70):
        #         print("opened sell position")
        #         sellposition = bTValues['bidclose'][ind] #askclose < bidclose initial pour profit
        #     if (buyposition == 0 and rsiList[-1] < 30):
        #         print("opened buy position")
        #         buyposition = bTValues['askclose'][ind] #bidclose > askclose inital pour profit
        #     # checkProfitLoss(ind, symbol, buyposition, sellposition)
        #     if (sellposition != 0 and sellposition - bTValues['askclose'][ind] > 0.001):
        #         profittrades += 1
        #         sellposition = 0
        #         print("profit made!")
        #     if (sellposition != 0 and sellposition - bTValues['askclose'][ind] < 0.001):
        #         sellposition = 0
        #         losstrades += 1
        #         print("loss made!")
        #     if (buyposition != 0 and buyposition - bTValues['bidclose'][ind] < 0.001):
        #         buyposition = 0
        #         profittrades +=1
        #         print("profit made!")
        #     if (buyposition != 0 and buyposition - bTValues['bidclose'][ind] > 0.001):
        #         buyposition = 0
        #         losstrades +=1
        #         print("loss made!")
        #     ind+=1
        # print("You made " + str(profittrades) + "profitable trades on " + symbol + " forex!")
        # print("You made " + str(losstrades) + "unprofitable trades on " + symbol + " forex!")


def liveApp():
    #while (True):
        # print(openSymbols)
        # print(symbols)
        # checkIfClosedPosition()
        # for symbol in symbols:
        #     rsiValue = getLastRsiValue(symbol)

        #     print(symbol + " RSI : " + str(rsiValue))

        #     if (rsiValue > upper_rsi):
        #         position(False, symbol) # Sell
        #         openSymbols.append(symbol)
        #         symbols.remove(symbol)
        #         #con.close()
        #         #exit(1)
        #     if (rsiValue < lower_rsi):
        #         position(True, symbol) # Buy
        #         openSymbols.append(symbol)
        #         symbols.remove(symbol)
        #         #con.close()
        #         #exit(1)
        # time.sleep(5)
        print("----------------");

con = fxcmpy.fxcmpy(access_token=token, log_level='error', server='demo', log_file='log.txt')

if (len(sys.argv) > 1 and sys.argv[1].lower() == '-b'):
    backTesting()
else:
    liveApp()

con.close()
