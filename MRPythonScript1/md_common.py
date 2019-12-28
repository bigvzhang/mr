# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 23:53:55 2017

@author: vic
"""

import ctypes
import sys
import time
import platform
import re

def printf(format, *args):
    sys.stdout.write(format % args)

if(platform.system() == "Windows") :
    dll = ctypes.cdll.LoadLibrary('MuRanZPython.dll')  
    #DLLCPY = ctypes.cdll.LoadLibrary('MSVCRT.DLL')  
else:
    dll = ctypes.CDLL('libMuRanZPython.so',mode=ctypes.RTLD_GLOBAL)


META_C_str         = ctypes.POINTER(ctypes.c_char) 
META_C_str_PTR     = ctypes.POINTER(META_C_str)
META_int32_PTR     = ctypes.POINTER(ctypes.c_int32)
META_void_PPTR     = ctypes.POINTER(ctypes.c_void_p)

dll.magd_qry_pre.argtypes = (ctypes.c_int, META_C_str_PTR, META_int32_PTR) # argv
dll.magd_qry.argtypes =     (ctypes.c_int, META_C_str_PTR, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p) # argv
dll.free_memory.argtypes = (ctypes.c_int, META_void_PPTR)# argvd
dll.dll_get_adjusted_trading_day.argtypes = (ctypes.c_int64, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int64))
dll.dll_get_ticket_price_by_ins.argtypes = (ctypes.c_char_p, ctypes.POINTER(ctypes.c_double))

dll.md_qry_pre.argtypes = (ctypes.c_int, META_C_str_PTR, META_int32_PTR) # argv
dll.md_qry.argtypes = (ctypes.c_int, META_C_str_PTR, ctypes.c_int, ctypes.c_char_p, META_int32_PTR, ctypes.c_void_p) # argv

def get_adjusted_trading_day(x1, x2):
    x = ctypes.c_int64(0)
    dll.dll_get_adjusted_trading_day(x1, x2.encode('utf8'), ctypes.pointer(x))
    return x.value

def get_ticket_price(x2):
    x = ctypes.c_double(0.0)
    dll.dll_get_ticket_price_by_ins(x2.encode('utf8'), ctypes.pointer(x))
    return x.value

class StructMRTime(ctypes.Structure):
        _fields_ = [
        ("Time",       ctypes.c_int64),
        ]
        
class StructMABasicData(ctypes.Structure):
       _fields_ = [
        ("Open",  ctypes.c_double),
        ("Last",  ctypes.c_double),
        ("High",  ctypes.c_double),
        ("Low",   ctypes.c_double),
        ("MA5",  ctypes.c_double),
        ("MA10",  ctypes.c_double),
        ("MA20",  ctypes.c_double),
        ]

class StructMABasicDataCollecton:
    my_tim_array  = (StructMRTime*1)()   
    my_array      = (StructMABasicData*1)()

def print_basic_ma_data(collection):
    rtn = len(collection.my_array)
    printf("%-25s", "Time")
    for field in StructMABasicData._fields_:
        printf("%-11s", field[0])
    print()
    for i in range(0, rtn):
        printf("%s.%03d", time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(collection.my_tim_array[i].Time / 1000)), collection.my_tim_array[i].Time % 1000)
        for field in StructMABasicData._fields_:
                 printf(" %10.3f",eval("collection.my_array[i].%s"%(field[0])))
        print()

def load_basic_ma_data(collection, till_date, instrument_id, used_interval, option_string = None):
    if(option_string is None or len(option_string) == 0):
        argc = 4
        argv         = (META_C_str*(argc))()
    else:
        vctString = option_string.split()
        argc = 4 + len(vctString)
        argv         = (META_C_str*(argc))()
        for i in range(0, len(vctString)):
            argv[4+i] = ctypes.create_string_buffer(vctString[i].encode("utf8"))
  
    argv[0] = ctypes.create_string_buffer(b"magd")
    argv[1] = ctypes.create_string_buffer(till_date.encode("utf8"))
    argv[2] = ctypes.create_string_buffer(instrument_id.encode("utf8"))
    argv[3] = ctypes.create_string_buffer(used_interval.encode("utf8"))

 
    rslt_cnt    = ctypes.c_int32(0)
    #rslt_v      = META_C_str()

    rtn = dll.magd_qry_pre(argc, argv, ctypes.pointer(rslt_cnt))
    
    str_fields_desc = ""
    for field in StructMABasicData._fields_:
       str_fields_desc=str_fields_desc + ("%s"%(eval("StructMABasicData.%s"%(field[0])))).replace("Field", field[0])
    str_fields_desc2 = ctypes.create_string_buffer(str_fields_desc.encode('utf-8'))
    if(rtn > 0):
        collection.my_tim_array  = (StructMRTime*rtn)()   
        collection.my_array      = (StructMABasicData*rtn)()
        rtn = dll.magd_qry(argc, argv, ctypes.sizeof(StructMABasicData), str_fields_desc2, ctypes.pointer(rslt_cnt),collection.my_tim_array, collection. my_array)
    return rtn

def print_basic_ma_data_structure():
    str_fields_desc = ""
    for field in StructMABasicData._fields_:
        print(field)
        str_fields_desc=str_fields_desc + ("%s"%(eval("StructMABasicData.%s"%(field[0])))).replace("Field", field[0])
    print(str_fields_desc)


###
###  The Following is for general structure
###       
    
       
def struct_factory(fields):
    return type("StructGeneralData", (ctypes.Structure,), {"_fields_": fields})

class StructGeneralDataCollecton:
    my_tim_array  = None #(StructMRTime*1)()   
    my_array      = None # (StructMABasicData*1)()
    data_struct   = None
    def __init__(self, data_fields):
        self.data_struct = struct_factory(data_fields)
    def insert_ahead(self, other):

        if(self.my_tim_array):
            tmp_tim_array  = self.my_tim_array
            tmp_data_array = self.my_array
            len_2 = len(other.my_tim_array)
            len_x = len(tmp_tim_array) + len_2
            self.my_tim_array  = (StructMRTime*len_x)()   
            self.my_array      = ((eval("self.data_struct"))*len_x)()
            for i in range(0, len(other.my_tim_array)):
                self.my_tim_array[i] = other.my_tim_array[i]
                #self.my_array[i]     = other.my_array[i]
                for field in self.data_struct._fields_:
                    exec("self.my_array[i].%s = other.my_array[i].%s"%(field[0], field[0]))

            for i in range(0, len(tmp_tim_array)):
                self.my_tim_array[i + len_2] = tmp_tim_array[i]
                self.my_array[i + len_2]     = tmp_data_array[i]
        else:
            len_x = len(other.my_tim_array)
            self.my_tim_array  = (StructMRTime*len_x)()   
            self.my_array      = ((eval("self.data_struct"))*len_x)()
            for i in range(0, len(other.my_tim_array)):
                self.my_tim_array[i] = other.my_tim_array[i]
                #self.my_array[i]     = other.my_array[i]
                for field in self.data_struct._fields_:
                    exec("self.my_array[i].%s = other.my_array[i].%s"%(field[0], field[0]))


class StructMDGeneralDataCollecton:
    my_array     = None # (StructMABasicData*1)()
    data_struct   = None
    def __init__(self, param_data_fields):
        fields2 = [ ("Time",       ctypes.c_int64),]
        fields2.extend(param_data_fields)
        self.data_struct = struct_factory(fields2)
        

def mrtime_to_std(t):   
    return "%s"%(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(t / 1000)))

def mrtime_to_yyyymmdd(t):
    return time.strftime("%Y%m%d",time.localtime(t / 1000))

def mrtime_to_std_milli(t):   
    return "%s.%03d"%(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(t / 1000)), t % 1000)

pattern_simple_date_format = re.compile(r"^[0-9]{4}(-){0,1}[0-9]{2}(-){0,1}[0-9]{2}(-){0,1}$")

def yyyymmdd_to_mrtime(s):
    mr = re.search(pattern_simple_date_format, s)
    if(mr):
        if(mr.group(1)):
            x = time.strptime(s, '%Y-%m-%d')
        else:
            x = time.strptime(s, '%Y%m%d')

        y = int(time.mktime(x))
        y *= 1000
        return y
    else:
        return 0
    
def mrtime_add_days(tim, d):
    return tim + d * 86400000


def print_general_ma_data(collection):
    rtn = len(collection.my_array)
    printf("%-25s", "Time")
    for field in collection.data_struct._fields_:
        printf("%-11s", field[0])
    print()
    for i in range(0, rtn):
        printf("%s.%03d", time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(collection.my_tim_array[i].Time / 1000)), collection.my_tim_array[i].Time % 1000)
        for field in collection.data_struct._fields_:
            printf(" %10.3f",eval("collection.my_array[i].%s"%(field[0])))
            #printf(" %s", field[0])

        print()

def load_general_ma_data(collection, till_date, instrument_id, used_interval, option_string = None):
    if(option_string is None or len(option_string) == 0):
        argc = 4
        argv         = (META_C_str*(argc))()
    else:
        vctString = option_string.split()
        argc = 4 + len(vctString)
        argv         = (META_C_str*(argc))()
        for i in range(0, len(vctString)):
            argv[4+i] = ctypes.create_string_buffer(vctString[i].encode("utf8"))
     
    
    argv[0] = ctypes.create_string_buffer(b"magd")
    argv[1] = ctypes.create_string_buffer(till_date.encode("utf8"))
    argv[2] = ctypes.create_string_buffer(instrument_id.encode("utf8"))
    argv[3] = ctypes.create_string_buffer(used_interval.encode("utf8"))
  
 
    rslt_cnt    = ctypes.c_int32(0)
    #rslt_v      = META_C_str()

    rtn = dll.magd_qry_pre(argc, argv, ctypes.pointer(rslt_cnt))
    
    str_fields_desc = ""
    #str_fields_desc_tmp=""
    for field in collection.data_struct._fields_:
        #print(field)
        #print(("%s"%(eval("StructMABasicData.%s"%(field[0])))).replace("Field", field[0]))
        #print(("%s"%(eval("collection.data_struct.%s"%(field[0])))).replace("Field", field[0]))
        str_fields_desc=str_fields_desc + ("%s"%(eval("collection.data_struct.%s"%(field[0])))).replace("Field", field[0])
        #str_fields_desc_tmp=str_fields_desc_tmp + ("%s"%(eval("StructMABasicData.%s"%(field[0])))).replace("Field", field[0])
    #if(str_fields_desc != str_fields_desc_tmp):
    #   exit(-1)
    str_fields_desc2 = ctypes.create_string_buffer(str_fields_desc.encode('utf-8'))
    if(rtn > 0):
        collection.my_tim_array  = (StructMRTime*rtn)()   
        collection.my_array      = ((eval("collection.data_struct"))*rtn)()
        rtn1 = dll.magd_qry(argc, argv, ctypes.sizeof((eval("collection.data_struct"))), str_fields_desc2, rslt_cnt, collection.my_tim_array, collection.my_array)
        if(rtn == rtn1):
            return rtn
        else:
            return rtn1
    else:
        return 0
    
def load_general_md_data(collection, till_date, instrument_id, option_string = None):
    if(option_string is None or len(option_string) == 0):
        argc = 4
        argv         = (META_C_str*(argc))()
    else:
        vctString = option_string.split()
        argc = 4 + len(vctString)
        argv         = (META_C_str*(argc))()
        for i in range(0, len(vctString)):
            argv[4+i] = ctypes.create_string_buffer(vctString[i].encode("utf8"))
     
    argv[0] = ctypes.create_string_buffer(sys.argv[0].encode('utf-8')) 
    argv[1] = ctypes.create_string_buffer(b"md")
    argv[2] = ctypes.create_string_buffer(till_date.encode("utf8"))
    argv[3] = ctypes.create_string_buffer(instrument_id.encode("utf8"))
  
 
    rslt_cnt    = ctypes.c_int32(0)
    #rslt_v      = META_C_str()

    rtn = dll.md_qry_pre(argc, argv, ctypes.pointer(rslt_cnt))
    
    #print("Found Reslt(%d)"%(rtn))
    
    str_fields_desc = ""
    #str_fields_desc_tmp=""
    collection2              = StructMDGeneralDataCollecton(collection.data_struct._fields_)

    for field in collection2.data_struct._fields_:
        str_fields_desc=str_fields_desc + ("%s"%(eval("collection2.data_struct.%s"%(field[0])))).replace("Field", field[0])

    str_fields_desc2 = ctypes.create_string_buffer(str_fields_desc.encode('utf-8'))
    if(rtn > 0):
        collection.my_tim_array  = (StructMRTime*rtn)()   
        collection.my_array      = ((eval("collection.data_struct"))*rtn)()
        collection2.my_array     =  ((eval("collection2.data_struct"))*rtn)()
        rtn1 = dll.md_qry(argc, argv, ctypes.sizeof((eval("collection2.data_struct"))), str_fields_desc2, rslt_cnt, collection2.my_array)
        for i in range(0, rtn):
            collection.my_tim_array[i].Time = collection2.my_array[i].Time
            for field in collection.data_struct._fields_:
                exec("collection.my_array[%d].%s = collection2.my_array[%d].%s"%(i,field[0],i,field[0]))
        if(rtn == rtn1):
            return rtn
        else:
            return rtn1
    else:
        return 0

