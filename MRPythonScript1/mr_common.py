# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 18:21:52 2017

@author: vic
"""
import time
import math

def mrtime_to_std(tim):
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(tim / 1000))

def mrtime_to_std_milli(tim):
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(tim / 1000)) + ".%03d"%(tim%1000)

def mrtime_to_str_date(tim, compact = False):
    if(compact):
        return time.strftime("%Y%m%d",time.localtime(tim / 1000))
    else:
        return time.strftime("%Y-%m-%d",time.localtime(tim / 1000))

def mrtime_span_to_std_str(e):
    a1 = int(e / 3600) * 3600
    a2 = int((e-a1)/ 60) * 60
    a3 = e - a1 - a2
    return "%02d:%02d:%06.3f"%(int(a1/3600), int(a2/60), a3)



def mr_get_close_divisors(n):
    x = int(math.sqrt(n))
    while(n%x != 0):
        x -= 1
    return x,int(n/x)

def mr_double2int(x):
    return int(x+0.5) if(x>0) else int(x-0.5)
  

