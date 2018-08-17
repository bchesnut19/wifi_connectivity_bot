#!/bin/python
###########################################################################
# Description:                                                            #
# Gets date from last line of wifi csv file                               #
###########################################################################

import datetime
import date_functions


def get_date():
   WIFI_CSV = open("/usr/local/projects/wifi_connectivity_bot/Record_Keeping/up_down_wifi.csv", "r")
   file_list = WIFI_CSV.readlines()
   WIFI_CSV.close()
   if len(file_list) < 3:
      return None
   else:
      last_date = date_functions.return_date(file_list[len(file_list)])
      return last_date

