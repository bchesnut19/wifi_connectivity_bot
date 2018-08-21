#!/bin/python
###########################################################################
# Description:                                                            #
# Gets date from last line of wifi csv file                               #
###########################################################################

import datetime
import date_functions

PATH = None

def init(path):
   global PATH
   PATH = path

def get_date():
   path = PATH + "Record_Keeping/up_down_wifi.csv"
   WIFI_CSV = open(path, "r")
   file_list = WIFI_CSV.readlines()
   WIFI_CSV.close()
   if len(file_list) < 3:
      return None
   else:
      last_date = date_functions.return_date(file_list[len(file_list)-1])
      return last_date

