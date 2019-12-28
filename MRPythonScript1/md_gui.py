# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 23:53:55 2017

@author: vic
"""
import time
import re
import os
from md_gui_common import *


def print_usage():
    print("Usage: md_gui 2017-09-08 ru1709 15M")
    
class MRGeneralEnvParams:
    def __init__(self):
              self.sim_date1 = ""
              self.sim_date2 = ""
              self.sim_time1 = ""
              self.sim_time2 = ""
              self.option_str = ""
              self.save_file= False
              self.save_file_as = ""
    def print_content(self):
        if(self.sim_date1 == self.sim_date2):
            print("Date Param:", self.sim_date1)
        else:
            print("Date Param:%s~%s"%(self.sim_date1, self.sim_date2))
        if(self.sim_time1 == self.sim_time2):
            print("Time Param:", self.sim_time1)
        else:
            print("Time Param:%s~%s"%(self.sim_time1, self.sim_time2))
        print("SaveFile(%s) FileName(%s)"%(self.save_file, self.save_file_as))
        if(self.option_str):
            print("Option:", self.option_str)


def parse_general_parameters(general_env):
    argc=(len(sys.argv))
    pattern_1  = re.compile(r"^(\d{8}|(\d{4}\-\d{2}\-\d{2}))(~(\d{8}|(\d{4}\-\d{2}\-\d{2}))){0,1}$")  
    pattern_2  = re.compile(r"^(\d{2}:\d{2}:\d{2})(~(\d{2}:\d{2}:\d{2})){0,1}")  
    for i in range(1, argc):
        if(not general_env.sim_date1): # Why not here, we allow input option string as date format
            rslt = re.search(pattern_1, sys.argv[i])
            if(rslt):
                general_env.sim_date1 = rslt.group(1)
                if(rslt.group(4)):
                    general_env.sim_date2 = rslt.group(4)
                else:
                    general_env.sim_date2 = general_env.sim_date1
                continue
        if(not general_env.sim_time1): # Why not here, we allow input option string as date format
            rslt = re.search(pattern_2, sys.argv[i])
            if(rslt):
                general_env.sim_time1 = rslt.group(1)
                if(rslt.group(3)):
                    general_env.sim_time2 = rslt.group(3)
                else:
                    general_env.sim_time2 = sim_time1
                continue
        if(sys.argv[i] == "--save"):
            general_env.save_file = True
            if(i + 1 < argc):
               general_env.save_file_as = sys.argv[i+1] 
               i = i+1
            continue
        
        if(not general_env.option_str):
            general_env.option_str  =  sys.argv[i]
        else:
            general_env.option_str  =  general_env.option_str + " " + sys.argv[i]

class MRGuiEnvParams(MRGeneralEnvParams):
      def __init__(self):
          super().__init__()
          parse_general_parameters(self)

          self.instrument_id = ""
          self.interval      = "5M"

          tmp_vct_str = self.option_str.split()
          self.option_str = ""
          found_ins      = False
          found_interval = False
          for s in tmp_vct_str:
              if(not found_ins):
                  if(re.match(r"^\w[\w-]*$", s)):
                      self.instrument_id = s
                      found_ins = True
                      continue
              if(not found_interval):
                  if(re.match(r"^\d+(M|S)$", s)):
                      self.interval = s
                      found_ins = True
                      continue
                  
              if(self.option_str):
                  self.option_str = s
              else:
                  self.option_str = self.option_str + " " + s
          if(not self.instrument_id):
              print(self.option_str)
              print_usage()
              exit(1)
          if(not self.sim_date1):
              self.sim_date1 = time.strftime('%Y-%m-%d')
              self.sim_date2 = self.sim_date1
          


env_params =    MRGuiEnvParams()
#env_params.print_content()


fig = plot_k(env_params.sim_date1, env_params.instrument_id, env_params.interval)
if(env_params.save_file):
    if(not env_params.save_file_as):
        file_name= "KChart_%s_%s.png"%(env_params.instrument_id, env_params.sim_date1.replace('-', ""))
    else:
        file_name = env_params.save_file_as
        if(not re.search("\.", file_name)):
            file_name = file_name + ".png"
    plt.savefig(file_name, dpi=80)
    print("OutputFile saved:", file_name)
plt.show()


