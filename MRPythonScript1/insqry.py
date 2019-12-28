import sys
import cfgapi


    
argc=(len(sys.argv))

def print_usage():
    print("Usage: FileName --get-prod ins_id")
    print("       FileName --prod-id  ins_id")

if(argc == 3):
    if(sys.argv[1] == '--prod-id' or sys.argv[1] == '--get-prod' ):
          rtn =  cfgapi.get_product_id_by_ins_id(sys.argv[2])
    else:
          print_usage()
          exit(1)
    print(" rtn:", rtn)
else:
    print_usage()
    exit(2)
    
exit(0)
    


