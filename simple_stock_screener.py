# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 09:50:27 2020

@author: Branson
"""
import numpy as np
from pandas_datareader import data as web
import datetime as dt
#import yfinance as yf
#yf.pdr_override()

def sma(values, window):
    weigths = np.repeat(1.0, window) / window
    smas = np.convolve(values, weigths, 'valid')

    return smas 

def rsi(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n + 1]
    up = seed[seed >= 0].sum() / n
    down = -seed[seed < 0].sum() / n
    rs = up / down
    r = np.zeros_like(prices)
    r[:n] = 100. - 100. / (1. + rs)

    for i in range(n, len(prices)):
        delta = deltas[i - 1]

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up * (n - 1) + upval) / n
        down = (down * (n - 1) + downval) / n

        rs = up / down
        r[i] = 100. - 100. / (1. + rs)

    return r


# 設定日期
start = dt.datetime(2019, 6, 19)
end = dt.datetime(2020, 6, 19)

# symlist
csv = open('symlist.csv', 'r', encoding= 'utf-8').read().split('\n')
sym_name = [s.split('	') for s in csv]
symlist = [s[0] for s in sym_name]  # ['0001.HK','0002.HK','0003.HK',...]
    

for s in sym_name:
    sym  = s[0]
    name = s[1]
    
    try:
        
        df = web.get_data_yahoo(sym, start, end)
        
        close = df['Close'].values
    
        sma60 = sma(close, 60)
        sma200 = sma(close, 200)
        rsi14 = rsi(close, 14)
        
        cond1,cond2,cond3,cond4,cond5 = False,False,False,False,False
    
        # 股價低於200天線, 濾掉
        if close[-1] > sma200[-1]:
            cond1 = True
        
        # 股價比前5天上升5%或以上
        if ((close[-1] / close[-5]) -1) * 100 > 5:
            cond2 = True
        
        # 股價的60天線和200天線呈現發散
        if (sma60[-1] - sma200[-2]) > (sma60[-2] - sma200[-2]):
            cond3 = True
        
        # RSI 大於50
        if rsi14[-1] > 50:
            cond4 = True
        
        # 股價連續二天向上突破
        if close[-1] > close[-2] and close[-2] > close[-3]:
            cond5 = True
    
        if cond1 and cond2 and cond3 and cond4 and cond5:
            print('股票 %s %s 符合模型' % (sym, name))
            
    except:
        continue