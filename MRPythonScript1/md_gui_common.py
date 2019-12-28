# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 15:33:20 2017

@author: vic
"""


import ctypes
from md_common import *

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches
import time
from dateutil.parser import parse
import numpy as np

import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
from numpy import *



def plot_k(param_date, instrument_id, param_interval):#(ticker, beginDate, endDate=datetime.date.today()):
    collection =   StructGeneralDataCollecton(
            [
            
            ("Open",  ctypes.c_double),
            ("Last",  ctypes.c_double),
            ("High",  ctypes.c_double),
            ("Low",   ctypes.c_double),
            ("Vol",   ctypes.c_double),
            
            ("MA5",   ctypes.c_double),
            ("MA10",  ctypes.c_double),
            ("MA26",  ctypes.c_double),
            ]
            )   
    load_general_ma_data(collection, param_date,instrument_id, param_interval)
    if(not collection.my_array):
        return None
    #print_general_ma_data(collection)
    #quotes = DataAPI.MktEqudAdjGet(ticker=ticker, beginDate=beginDate, endDate=endDate, isOpen='1',field=["secShortName","ticker","openPrice","closePrice","highestPrice","lowestPrice","tradeDate","dealAmount","isOpen"])
    #dt_new = cal.advanceDate(beginDate, '-100B', BizDayConvention.Following)
    #quotes2 = DataAPI.MktEqudAdjGet(ticker=ticker, beginDate=dt_new, endDate=endDate, isOpen='1',field=["secShortName","ticker","openPrice","closePrice","highestPrice","lowestPrice","tradeDate","dealAmount","isOpen"])
    quotes_idx = []
    data_len = len(collection.my_array)
    for i in range(0, data_len ):
        quotes_idx.append("%s"%(time.strftime("%m-%d %H:%M",time.localtime(collection.my_tim_array[i].Time / 1000))))

    __color_balck__= '#000000'
    __color_green__= '#00FFFF'
    __color_purple__ = '#9900CC'
    __color_golden__= '#FFD306'


    fig = plt.figure(figsize=(10,5))
    fig.set_tight_layout(False)
    #plt.subplot(211)
    ax1 = fig.add_axes([0.06, 0.35, 0.93, 0.60])
    ax1.set_title("%s(%s)"%(param_date, param_interval))
    ax1.set_axisbelow(True)
    #plt.subplot(212)
    #ax2 = fig.add_axes([0, 0.35, 1, 0.5], axis_bgcolor='w')
    ax2 = fig.add_axes([0.06, 0.05, 0.93, 0.20])
    ax2.set_axisbelow(True)
    ax1.grid(True)
    ax2.grid(True)
    ax1.set_xlim(-1, data_len+2)
    ax2.set_xlim(-1, data_len+2)
    vol_max = 0
    for i in range(data_len):
        close_price = collection.my_array[i].Last
        open_price =  collection.my_array[i].Open
        high_price =  collection.my_array[i].High
        low_price =   collection.my_array[i].Low
        vol      =    collection.my_array[i].Vol
        if(vol > vol_max):
            vol_max = vol
        #trade_date = quotes_idx[i]
        if close_price > open_price:
            ax1.add_patch(patches.Rectangle((i-0.2, open_price), 0.4, close_price-open_price, fill=False, color='r'))
            ax1.plot([i, i], [low_price, open_price], 'r')
            ax1.plot([i, i], [close_price, high_price], 'r')
            ax2.add_patch(patches.Rectangle((i-0.2, 0), 0.4, vol, fill=False, color='r'))
            #ax2.add_patch(patches.Rectangle((i-0.2, open_price), 0.4, close_price-open_price, fill=False, color='r'))
        else:
            ax1.add_patch(patches.Rectangle((i-0.2, open_price), 0.4, close_price-open_price, color='g'))
            ax1.plot([i, i], [low_price, high_price], color='g')
            #ax2.add_patch(patches.Rectangle((i-0.2, open_price), 0.4, close_price-open_price, color='g'))
            ax2.add_patch(patches.Rectangle((i-0.2, 0), 0.4, vol, color='g'))
    ax2.set_ylim(0,  int(vol_max*1.1))
    #ax1.set_title(instrument_id, fontproperties=font, fontsize=15, loc='left', color='r')
    #ax2.set_title(u'成交量', fontproperties=font, fontsize=15, loc='left', color='r')
    ax1.set_title(instrument_id, fontsize=15, loc='left', color='r')
    ax2.set_title(u'Volume', fontsize=15, loc='left', color='r')

    xticks_cnt = int(data_len/8)
    if( xticks_cnt < 8):
        xticks_cnt = 8
    ax1.set_xticks(range(0,data_len, xticks_cnt))
    ax2.set_xticks(range(0,data_len, xticks_cnt)) 
    s1 = ax1.set_xticklabels([quotes_idx[index] for index in ax1.get_xticks()])
    s2 = ax2.set_xticklabels([quotes_idx[index] for index in ax2.get_xticks()])
         
#    ma5 = pd.rolling_mean(np.array(quotes2['closePrice'], dtype=float), window=5, min_periods=0)[-len(quotes):]
#    ma10 = pd.rolling_mean(np.array(quotes2['closePrice'], dtype=float), window=10, min_periods=0)[-len(quotes):]
#    ma20 = pd.rolling_mean(np.array(quotes2['closePrice'], dtype=float), window=20, min_periods=0)[-len(quotes):]
#    ma96 = pd.rolling_mean(np.array(quotes2['closePrice'], dtype=float), window=96, min_periods=0)[-len(quotes):]
#
#    ax1.plot(ma5, color='b')
#    ax1.plot(ma10, color='y')
#    ax1.plot(ma20, color=__color_purple__)
#    ax1.plot(ma96, color=__color_golden__)
#    
#    ax1.annotate('MA5-', xy=(len(quotes)-32, ax1.get_yticks()[-1]), color='b', fontsize=10)
#    ax1.annotate('MA10-', xy=(len(quotes)-24, ax1.get_yticks()[-1]), color='y', fontsize=10)
#    ax1.annotate('MA20-', xy=(len(quotes)-16, ax1.get_yticks()[-1]), color=__color_purple__, fontsize=10)
#    ax1.annotate('MA96-', xy=(len(quotes)-8, ax1.get_yticks()[-1]), color=__color_golden__, fontsize=10)
#    vol5 = pd.rolling_mean(np.array(quotes['dealAmount'], dtype=float), window=5, min_periods=0)
#    vol10 = pd.rolling_mean(np.array(quotes['dealAmount'], dtype=float), window=10, min_periods=0)
#    ax2.plot(vol5, color='b')
#    ax2.plot(vol10, color='y')
    return fig