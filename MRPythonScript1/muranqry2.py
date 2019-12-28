# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 02:11:40 2017

@author: vic
"""
import ctypes
import sys
import time
import platform
import re
import md_common as md_api

fieldsX= [
        ("LastPrice",  ctypes.c_double),
        ("Volume",     ctypes.c_int32)]


argc = len(sys.argv) 

cfg_file = "mrai.conf"
obj_input = ""
obj_req   = ""
sim_date1  = ""
sim_date2  = ""
sim_time1  = ""
sim_time2  = ""
instrument_id = ""
option_str = ""
print_param = False

if(argc >= 2):
    obj_input = sys.argv[1]
    
    #pattern_1  = re.compile(r"^(\d{8}||(\d{4}-\d{2}-\d{2}))|(~(\d{8}||(\d{4}-\d{2}-\d{2}))){0,1}$")  
    #pattern_1  = re.compile(r"^(\d{8}|(\d{4}\-\d{2}\-\d{2}))$")  
    pattern_1  = re.compile(r"^(\d{8}|(\d{4}\-\d{2}\-\d{2}))(~(\d{8}|(\d{4}\-\d{2}\-\d{2}))){0,1}$")  
    pattern_2  = re.compile(r"^(\d{2}:\d{2}:\d{2})(~(\d{2}:\d{2}:\d{2})){0,1}")  
    pattern_3  = re.compile(r"([a-zA-Z]+\d+|[a-zA-Z]+\d+\-{0,1}[PC]\-{0,1}\d+)")
    for i in range(1, argc):
        if(not sim_date1): # Why not here, we allow input option string as date format
            rslt = re.search(pattern_1, sys.argv[i])
            if(rslt):
                sim_date1 = rslt.group(1)
                if(rslt.group(4)):
                    sim_date2 = rslt.group(4)
                else:
                    sim_date2 = sim_date1
#                if(sim_date1 == sim_date2):
#                    print("Date Param:", sim_date1)
#                else:
#                    print("Date Param:%s~%s"%(sim_date1, sim_date2))
                continue
        if(not sim_time1): # Why not here, we allow input option string as date format
            rslt = re.search(pattern_2, sys.argv[i])
            if(rslt):
                sim_time1 = rslt.group(1)
                if(rslt.group(3)):
                    sim_time2 = rslt.group(3)
                else:
                    sim_time2 = sim_time1
#                if(sim_time1 == sim_time2):
#                    print("Time Param:", sim_time1)
#                else:
#                    print("Time Param:%s~%s"%(sim_time1, sim_time2))
                continue
        if(sys.argv[i] == "--debug"):
            print_param = True
            continue
        if(not instrument_id):
            rslt = re.search(pattern_3, sys.argv[i])
            if(rslt):
                instrument_id = rslt.group(1)
                continue
            
        if(not option_str):
            option_str = sys.argv[i]
        else:
            option_str = option_str + " " + sys.argv[i]
        #print("Normal Param:", sys.argv[i])
else:
    print_usage()
    sys.exit(2)

print("Date:%s ID:%s"%(sim_date1, instrument_id))


collection = md_api.StructGeneralDataCollecton(fieldsX)

if(md_api.load_general_md_data(collection, sim_date1, instrument_id, option_str) > 0):
    md_api.print_general_ma_data(collection)

