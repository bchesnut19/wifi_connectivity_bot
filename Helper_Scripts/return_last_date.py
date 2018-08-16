#!/bin/python
###########################################################################
# Description:                                                            #
# Gets date from last line of wifi csv file                               #
###########################################################################

import datetime
import date_functions

WIFI_CSV = open("/usr/local/projects/wifi_connectivity_bot/Record_Keeping/up_down_wifi.csv", "r")

def get_date():
   file_list = WIFI_CSV.readlines()
   if len(file_list) < 3:
      return None
   else:
      last_date = date_functions.return_date(file_list[len(file_list)-1])
      return last_date

