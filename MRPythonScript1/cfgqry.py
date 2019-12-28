import sys
import cfgapi


    
argc=(len(sys.argv))
#for i, arg in enumerate(sys.argv):
#    print("%d OF(%d)=>%s"%(i,argc,arg))


if(argc == 3):
    rtn = cfgapi.get_cfg_string_value(sys.argv[1], sys.argv[2])
    print(" rtn:", rtn)
elif(argc == 4):
    if(sys.argv[2] == '--keys'):
          rtn =  cfgapi.get_cfg_child_keys(sys.argv[1], sys.argv[3])
    elif(sys.argv[3] == '--keys'):
          rtn =  cfgapi.get_cfg_child_keys(sys.argv[1], sys.argv[2])
    else:
          rtn = cfgapi.get_cfg_pc_string_value(sys.argv[1], sys.argv[2], sys.argv[3])
    print(" rtn:", rtn)
elif(argc == 5):
    parameters = []
    req_typ = "--string"
    for i in range(1,5):
        if(sys.argv[i] == "--int"):
            req_typ = "--int"
        elif(sys.argv[i] == "--dbl"):
            req_typ = "--dbl"
        elif(sys.argv[i] == "--bool"):
            req_typ = "--bool"   
        elif(sys.argv[i][0] == '-'):
            print("Invalid Option %s"%(sys.argv[i]))
            sys.exit(-1)
        else:
            parameters.append(sys.argv[i])
    #print("req_typ", req_typ)     
    if(req_typ == '--int'):
        rtn = cfgapi.get_cfg_pc_int_value(parameters[0],parameters[1], parameters[2], 0)
        print(" rtn:", rtn, " <=Type(%s)"%(type(rtn)))
    elif(req_typ == '--dbl'):
        rtn = cfgapi.get_cfg_pc_dbl_value(parameters[0],parameters[1], parameters[2], 0.0)
        print(" rtn:", rtn, " <=Type(%s)"%(type(rtn)))
    elif(req_typ == '--bool'):
        rtn = cfgapi.get_cfg_pc_bool_value(parameters[0],parameters[1], parameters[2], False)
        print(" rtn:", rtn, " <=Type(%s)"%(type(rtn)))
    elif(req_typ == '--string'):
        rtn = cfgapi.get_cfg_pc_string_value(parameters[0],parameters[1], parameters[2])
        print(" rtn:", rtn)
    else:
        print("Bad Data Integrity")
        sys.exit(-1)

else:
    print("Usage: FileName KeyPath")
    print("       FileName KeyPath pc_parameter")
    print("       FileName KeyPath pc_parameter --(int|dbl|bool)")
    print("       pc_parameter ")

    sys.exit(2)
    
sys.exit(0)
    


