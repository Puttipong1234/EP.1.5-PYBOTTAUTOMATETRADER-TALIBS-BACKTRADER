import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.signal import find_peaks , peak_prominences

import talib
from line_notify import LineNotify

from config import binance_api_key , binance_api_secret , Line_token
from binance.client import Client # ccxt 

client = Client(binance_api_key , binance_api_secret)

def GetAnalysisTA(symbolname):
    symbol = symbolname
    day = 10
    klines = client.get_historical_klines( symbol , Client.KLINE_INTERVAL_1HOUR , "{} day ago UTC".format(day) )

    # for i in klines:
    #     print(i)

    close = [ float(i[4]) for i in klines] # list comprehension
    close = np.array(close)
    invert_close = [ float(i[4])*-1 for i in klines]
    invert_close = np.array(invert_close)

    #plot boilinger band
    upperband, middleband, lowerband = talib.BBANDS(close, timeperiod=10 , matype=talib.MA_Type.EMA)

    # EMA 20 , 50
    ema20 = talib.EMA(close , timeperiod=20)
    ema50 = talib.EMA(close , timeperiod=50)

    # Find peak and valley
    peaks , _ = find_peaks(close , threshold=0.7)
    valley , _ = find_peaks(invert_close , threshold=0.7)

    #plot จุดตัด crossover crossunder
    crossup = []
    crossdown = []
    for index , (i,j) in enumerate(zip(ema20,ema50)):
        if i == np.NAN or j == np.NAN:
            continue
        #cross up
        if i > j and ema20[index-1] < ema50[index-1]:
            crossup.append(index)
        #cross down
        elif i < j and ema20[index-1] > ema50[index-1]:
            crossdown.append(index)

    # Create plot
    fig = plt.figure()
    axes = fig.add_axes([0.1,0.1,0.8,0.8])
    axes.set_xlabel("1 hour - Timeframe")
    axes.set_ylabel("PRICE")
    axes.set_title(symbol)
    # plot price
    plt.plot(close,color="blue")

    # plot BBANDS
    plt.plot(upperband , "--" , label="UPB" , color="grey")
    plt.plot(lowerband , "--" , label="LWB" , color="grey")

    #plot EMA
    plt.plot(ema20 , "--" , label="UPB" , color="green")
    plt.plot(ema50 , "--" , label="LWB" , color="red")

    #plot peak , valley
    plt.plot(peaks , close[peaks] , "." , color= "grey")
    plt.plot(valley , close[valley] , "." , color= "grey")

    #plot จุดตัด crossover crossunder
    offset = close*0.05
    crossup = np.array(crossup)
    crossdown = np.array(crossdown)
    plt.plot(crossup,close[crossup],"^" , color="green")
    plt.plot(crossdown,close[crossdown],"v" , color="red")

    # add legend
    plt.legend(loc="upper left")

    # plt.show()
    fig.set_size_inches(15,8)
    plt.savefig('fig/figure.png',dpi=100)
    plt.close()

    # notify to chat room
    notify = LineNotify(Line_token, name="PYBOTT")
    notify.send(symbol)
    notify.send("มีสัญญาณดังภาพ", image_path='fig/figure.png')
