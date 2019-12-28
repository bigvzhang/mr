import ctypes
import sys
#import time
import platform
import re
#from datetime import datetime

if(platform.system() == "Windows") :
    dll = ctypes.cdll.LoadLibrary('MuRanZPython.dll')  
else:
    dll = ctypes.cdll.LoadLibrary('libMuRanZPython.so')  

META_C_str         = ctypes.POINTER(ctypes.c_char) 
META_C_str_PTR     = ctypes.POINTER(META_C_str)
META_int32_PTR     = ctypes.POINTER(ctypes.c_int32)
META_void_PPTR     = ctypes.POINTER(ctypes.c_void_p)
META_dbl_PTR       = ctypes.POINTER(ctypes.c_double)

 
#bool get_cfg_string_value(const char* filepath, const char * parameter_path, char* buff, int buff_size, int* rtn_str_size);
#int get_cfg_pc_string_value(const char* filepath, const char * cfg_key, const char * pc_path, char* buff, int buff_size, int* rtn_str_size){
dll.get_cfg_string_value.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int32, META_int32_PTR) # argv
dll.get_cfg_child_keys.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int32, META_int32_PTR) # argv
dll.get_cfg_pc_string_value.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int32, META_int32_PTR) # argv
dll.get_cfg_pc_int_value.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, META_int32_PTR) # argv
dll.get_cfg_pc_dbl_value.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, META_dbl_PTR) # argv
dll.dll_get_prod_id_by_ins_id.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int32, META_int32_PTR) # argv
#int dll_handle_mutations(const char* base_dir, const char* cfg_file, const char* involved_paths, int mutation_id, const char* content, int action_if_conflicts);
dll.dll_handle_mutations.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int32, ctypes.c_char_p, ctypes.c_int32) # argv
#int dll_show_mutations(const char* base_dir, const char* cfg_file, const char* involved_paths,  const char* ids);
dll.dll_show_mutations.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p) # argv
dll.dll_get_mutation_cfg.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int32, ctypes.c_char_p, ctypes.c_int32, META_int32_PTR) # argv
dll.dll_delete_mutations.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p) # argv

def get_cfg_cstring_value(param__file_path,  param__cfg_path):
    buff_size   = 30
    buff        = ctypes.create_string_buffer(buff_size)
    buff_len    = ctypes.c_int32(buff_size)
    rslt_cnt    = ctypes.c_int32(0)
    file_path   = ctypes.create_string_buffer(param__file_path.encode('utf8'))
    cfg_path    = ctypes.c_char_p(param__cfg_path.encode('utf8'))
    rtn1 = dll.get_cfg_string_value(file_path, cfg_path, buff, buff_len, ctypes.pointer(rslt_cnt))
#    print("rslt:", rtn1)
#    print("file:", repr(file_path.value))
#    print("path:", repr(parameter_path.value))
#    print("buff:", repr(buff.value))
#    print(" cnt:", rslt_cnt)
    if(rtn1):
        return buff
    else:
        if(rslt_cnt.value > buff_len.value):
            buff_len =  rslt_cnt
            buff     =  ctypes.create_string_buffer(rslt_cnt.value)
            rtn1 = dll.get_cfg_string_value(file_path, cfg_path, buff, buff_len, ctypes.pointer(rslt_cnt))
    return buff

def get_cfg_string_value(param__file_path,  param__cfg_path):
    return get_cfg_cstring_value(param__file_path, param__cfg_path).value.decode('utf8')

def get_cfg_child_keys(param__file_path,  param__cfg_path):
    buff_size   = 100
    buff        = ctypes.create_string_buffer(buff_size)
    buff_len    = ctypes.c_int32(buff_size)
    rslt_cnt    = ctypes.c_int32(0)
    file_path   = ctypes.create_string_buffer(param__file_path.encode('utf8'))
    cfg_path    = ctypes.c_char_p(param__cfg_path.encode('utf8'))
    rtn1 = dll.get_cfg_child_keys(file_path, cfg_path, buff, buff_len, ctypes.pointer(rslt_cnt))
#    print("rslt:", rtn1)
#    print("file:", repr(file_path.value))
#    print("path:", repr(parameter_path.value))
#    print("buff:", repr(buff.value))
#    print(" cnt:", rslt_cnt)
    if(rtn1):
        return buff
    else:
        if(rslt_cnt.value > buff_len.value):
            buff_len =  rslt_cnt
            buff     =  ctypes.create_string_buffer(rslt_cnt.value)
            rtn1 = dll.get_cfg_child_keys(file_path, cfg_path, buff, buff_len, ctypes.pointer(rslt_cnt))
    return buff

def get_product_id_by_ins_id__cstring(param__ins_id):
    buff_size   = 30
    buff        = ctypes.create_string_buffer(buff_size)
    buff_len    = ctypes.c_int32(buff_size)
    rslt_cnt    = ctypes.c_int32(0)
    ins_id    = ctypes.c_char_p(param__ins_id.encode('utf8'))
    rtn1 = dll.dll_get_prod_id_by_ins_id(ins_id, buff, buff_len, ctypes.pointer(rslt_cnt))
#    print("rslt:", rtn1)
#    print("path:", repr(parameter_path.value))
#    print("buff:", repr(buff.value))
#    print(" cnt:", rslt_cnt)
    if(rtn1):
        return buff
    else:
        if(rslt_cnt.value > buff_len.value):
            buff_len =  rslt_cnt
            buff     =  ctypes.create_string_buffer(rslt_cnt.value)
            rtn1 = dll.dll_get_prod_id_by_ins_id(ins_id, buff, buff_len, ctypes.pointer(rslt_cnt))
    return buff

def get_product_id_by_ins_id(param__ins_id):
    return get_product_id_by_ins_id__cstring(param__ins_id).value.decode('utf8')
    
def get_cfg_pc_cstring_value(param__file_path,  param__cfg_path, param__pc_path):
    buff_size   = 30
    buff        = ctypes.create_string_buffer(buff_size)
    buff_len    = ctypes.c_int32(buff_size)
    rslt_cnt    = ctypes.c_int32(0)
    file_path   = ctypes.create_string_buffer(param__file_path.encode('utf8'))
    cfg_path    = ctypes.c_char_p(param__cfg_path.encode('utf8'))
    pc_path     = ctypes.c_char_p(param__pc_path.encode('utf8'))

    rtn1 = dll.get_cfg_pc_string_value(file_path, cfg_path, pc_path, buff, buff_len, ctypes.pointer(rslt_cnt))
#    print("rslt:", rtn1)
#    print("file:", repr(file_path.value))
#    print(" cfg:", repr(parameter_path.value))
#    print("buff:", repr(buff.value))
#    print(" cnt:", rslt_cnt)
    if(rtn1):
        return buff
    else:
        if(rslt_cnt.value > buff_len.value):
            buff_len =  rslt_cnt
            buff     =  ctypes.create_string_buffer(rslt_cnt.value)
            rtn1 = dll.get_cfg_pc_string_value(file_path, cfg_path, pc_path, buff, buff_len, ctypes.pointer(rslt_cnt))
    return buff

def get_cfg_pc_string_value(param__file_path,  param__cfg_path, param__pc_path, empty_default=''):
    rtn = get_cfg_pc_cstring_value(param__file_path,  param__cfg_path, param__pc_path).value.decode('utf8')
    return rtn if(len(rtn) > 0) else empty_default

def get_cfg_replaced_string_value(param__file_path,  param__cfg_path):
    s1 = get_cfg_string_value(param__file_path, param__cfg_path)
    s2 = get_cfg_pc_string_value(param__file_path,  param__cfg_path, "")
    s2 = s2.strip()
    if(len(s2) == 0):
        return s1
    else:
        pattern_1 =  re.compile(r"parameters:((\S+)$|(\S+)\s)")
        mr = re.search(pattern_1, s1)
        if(mr):
            if(not mr.group(2) is None):
                s1 = re.sub(r"parameters:(\S+)$", "parameters:%s"%(s2), s1)
            else:
                s1 = re.sub(r"parameters:(\S+)\s", "parameters:%s "%(s2), s1) #adding one space
            return s1
        else:
            return s1
  
    
def get_cfg_pc_int_value(param__file_path,  param__cfg_path, param__pc_path, default_v):
    file_path   = ctypes.create_string_buffer(param__file_path.encode('utf8'))
    cfg_path    = ctypes.c_char_p(param__cfg_path.encode('utf8'))
    pc_path     = ctypes.c_char_p(param__pc_path.encode('utf8'))
    rslt_int    = ctypes.c_int32(0)
    rtn1 = dll.get_cfg_pc_int_value(file_path, cfg_path, pc_path,ctypes.pointer(rslt_int))
    if(rtn1 == 1):
        return rslt_int.value
    else:
        return default_v

def get_cfg_pc_dbl_value(param__file_path,  param__cfg_path, param__pc_path, default_v):
    file_path   = ctypes.create_string_buffer(param__file_path.encode('utf8'))
    cfg_path    = ctypes.c_char_p(param__cfg_path.encode('utf8'))
    pc_path     = ctypes.c_char_p(param__pc_path.encode('utf8'))
    rslt_dbl    = ctypes.c_double(0)
    rtn1 = dll.get_cfg_pc_dbl_value(file_path, cfg_path, pc_path,ctypes.pointer(rslt_dbl))
    if(rtn1 == 1):
        return rslt_dbl.value
    else:
        return default_v
    
def get_cfg_pc_bool_value(param__file_path,  param__cfg_path, param__pc_path, default_v):
    s = get_cfg_pc_string_value(param__file_path,  param__cfg_path, param__pc_path)
    if(s is None or len(s) == 0):
        return default_v
    if(re.match(r"^(True|1)$", s,  re.IGNORECASE)):
        return True
    elif(re.match(r"^(False|0)$", s,  re.IGNORECASE)):
        return False
    else:
        print("Warn!!!, Required bool Type For(@%s, %s : %s), but given (%s); Default(%s)"
              %(param__file_path,  param__cfg_path, param__pc_path, s, default_v))
        return default_v
    
def handle_mutations(param_base_dir, param_cfg_file, param_involved_paths, param_mutation_id, param_content, param_action_if_conflicts):
    base_dir    = ctypes.c_char_p(param_base_dir.encode('utf8'))
    cfg_file    = ctypes.c_char_p(param_cfg_file.encode('utf8'))
    involved_paths    = ctypes.c_char_p(param_involved_paths.encode('utf8'))
    mutation_id = ctypes.c_int32(param_mutation_id)
    content    = ctypes.c_char_p(param_content.encode('utf8'))
    action     = ctypes.c_int32(param_action_if_conflicts)
    return dll.dll_handle_mutations(base_dir, cfg_file, involved_paths, mutation_id, content, action)
 
def show_mutations(param_base_dir, param_cfg_file, param_involved_paths, param_ids, param_prompt):
    base_dir    = ctypes.c_char_p(param_base_dir.encode('utf8'))
    cfg_file    = ctypes.c_char_p(param_cfg_file.encode('utf8'))
    involved_paths    = ctypes.c_char_p(param_involved_paths.encode('utf8'))
    ids         = ctypes.c_char_p(param_ids.encode('utf8'))
    prompt      = ctypes.c_char_p(param_prompt.encode('utf8'))
    return dll.dll_show_mutations(base_dir, cfg_file, involved_paths, ids, prompt)

def get_mutation_cfg_cstring(param_base_dir, param_cfg_file, param_involved_paths, param_mutation_id):
    base_dir    = ctypes.c_char_p(param_base_dir.encode('utf8'))
    cfg_file    = ctypes.c_char_p(param_cfg_file.encode('utf8'))
    involved_paths    = ctypes.c_char_p(param_involved_paths.encode('utf8'))
    mutation_id = ctypes.c_int32(param_mutation_id)
    
    buff_size   = 30
    buff        = ctypes.create_string_buffer(buff_size)
    buff_len    = ctypes.c_int32(buff_size)
    rslt_cnt    = ctypes.c_int32(0)


    rtn1 = dll.dll_get_mutation_cfg(base_dir, cfg_file, involved_paths, mutation_id, buff, buff_len, ctypes.pointer(rslt_cnt))
    if(rtn1):
        return buff
    else:
        if(rslt_cnt.value > buff_len.value):
            buff_len =  rslt_cnt
            buff     =  ctypes.create_string_buffer(rslt_cnt.value)
            rtn1 = dll.dll_get_mutation_cfg(base_dir, cfg_file, involved_paths, mutation_id, buff, buff_len, ctypes.pointer(rslt_cnt))
            return buff
        else:
            return None
        
def get_mutation_cfg(param_base_dir, param_cfg_file, param_involved_paths, param_mutation_id):
    rtn = get_mutation_cfg_cstring(param_base_dir, param_cfg_file, param_involved_paths, param_mutation_id)
    if(rtn is None):
        return ""
    else:
        return rtn.value.decode('utf8')
    
def delete_mutations(param_base_dir, param_cfg_file, param_involved_paths, param_ids):
    base_dir    = ctypes.c_char_p(param_base_dir.encode('utf8'))
    cfg_file    = ctypes.c_char_p(param_cfg_file.encode('utf8'))
    involved_paths    = ctypes.c_char_p(param_involved_paths.encode('utf8'))
    ids         = ctypes.c_char_p(param_ids.encode('utf8'))
    return dll.dll_delete_mutations(base_dir, cfg_file, involved_paths, ids)




