import ctypes
import sys
import time
import platform
#from datetime import datetime

def printf(format, *args):
    sys.stdout.write(format % args)

if(platform.system() == "Windows") :
    dll = ctypes.cdll.LoadLibrary('MuRanZPython.dll')  
    #DLLCPY = ctypes.cdll.LoadLibrary('MSVCRT.DLL')  
else:
    dll = ctypes.cdll.LoadLibrary('libMuRanZPython.so')  


argc = len(sys.argv) 


META_C_str         = ctypes.POINTER(ctypes.c_char) 
META_C_str_PTR     = ctypes.POINTER(META_C_str)
META_int32_PTR     = ctypes.POINTER(ctypes.c_int32)
META_void_PPTR     = ctypes.POINTER(ctypes.c_void_p)

dll.magd_qry_pre.argtypes = (ctypes.c_int, META_C_str_PTR, META_int32_PTR) # argv
dll.magd_qry.argtypes =     (ctypes.c_int, META_C_str_PTR, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p) # argv
dll.free_memory.argtypes = (ctypes.c_int, META_void_PPTR)# argvd
#DLLCPY.memcpy.argtypes   = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int64) # argv

argv         = (META_C_str*(argc + 1))()

rslt_cnt    = ctypes.c_int32(0)
rslt_v      = META_C_str()
for i, arg in enumerate(sys.argv):
    enc_arg = arg.encode('utf-8') 
    argv[i] = ctypes.create_string_buffer(enc_arg)
    #print("%d OF(%d)=>%s"%(i,argc,arg))
    
class StructMRTime(ctypes.Structure):
        _fields_ = [
        ("Time",       ctypes.c_int64),
        ]
class StructData(ctypes.Structure):
       _fields_ = [
        ("Open",  ctypes.c_double),
        ("Last",  ctypes.c_double),
        ("High",  ctypes.c_double),
        ("Low",   ctypes.c_double),
        ("MA5",   ctypes.c_double),
        ("MA10",  ctypes.c_double),
        ("MA20",  ctypes.c_double),
        ("BZ0",   ctypes.c_double),
        ("BZ1",   ctypes.c_double),
        ("BZ2",   ctypes.c_double),
        
        ]
#        ('Flag',       ctypes.c_char)]
#print("rslt cnt:", rslt_cnt)
#print("rslt cnt:", rslt_v)
rtn1 = dll.magd_qry_pre(argc, argv, ctypes.pointer(rslt_cnt))
#print("rtn",       rtn)
#print("rslt cnt:", rslt_cnt)
#print("rslt cnt(%d)(Address:%I64X)"%(rslt_cnt, rslt_v))
#my_struct = ctypes.cast(rslt_v, ctypes.POINTER(StructTest))

str_fields_desc = ""
for field in StructData._fields_:
   str_fields_desc=str_fields_desc + ("%s"%(eval("StructData.%s"%(field[0])))).replace("Field", field[0])
str_fields_desc2 = ctypes.create_string_buffer(str_fields_desc.encode('utf-8'))
if(rtn1 <= 0):
     print("No Data Found")
else:
#    print("Rtn", rtn, "rslt_rtn", rslt_cnt)
    my_tim_array  = (StructMRTime*rtn1)()   
    my_array      = (StructData*rtn1)()
    #print("echo from python=>"+str_fields_desc)
    rtn = dll.magd_qry(argc, argv, ctypes.sizeof(StructData), str_fields_desc2, rslt_cnt, my_tim_array, my_array)
#    print("Rtn", rtn, "rslt_rtn", rslt_cnt)

    #print("my struct:", my_array)
    printf("%-25s", "Time")
    for field in StructData._fields_:
        printf("%-11s", field[0])
    
    print()
    for i in range(0, rtn):
        printf("%s.%03d", time.strftime("%Y-%m-%d %H:%M:%S",time.localtime( my_tim_array[i].Time / 1000)), my_tim_array[i].Time % 1000)
        for field in StructData._fields_:
                 printf(" %10.3f",eval("my_array[i].%s"%(field[0])))
        print()
    if(rtn == rtn1):
        print("-----%s Records--------"%rtn)
    else:
        print("-----(%s %s) Records--------"%(rtn1, rtn))

#         printf("%s.%03d %10.3f\n", 
#                time.strftime("%Y-%m-%d %H:%M:%S",time.localtime( my_array[i].Time / 1000)), my_array[i].Time % 1000,
#                my_array[i].LastPrice)

#print("my struct:", my_array, "sizeofstruct(%d)"%(ctypes.sizeof(StructTest)))
#
#x = StructTest()
#print(str_fields_desc)
#print(StructTest)
#print(StructTest.Time)
#
#
#for field in StructTest._fields_:
#    print(field)
#    for item in field:
#        print(item, type(item))


#dll.free_memory(0, ctypes.pointer(rslt_v))


