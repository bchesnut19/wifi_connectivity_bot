#!/bin/python
###########################################################################
# Description:                                                            #
# Gets date from last line of wifi csv file                               #
###########################################################################

import datetime

WIFI_CSV = open("/usr/local/projects/wifi_connectivity_bot/Record_Keeping/up_down_wifi.csv", "r")

def get_date():
   csv_list = WIFI_CSV.readlines()
   if len(csv_list) < 3:
      return None
   else:
      last_line = csv_list[len(csv_list)-1]
      line_list = last_line.split(',')
   
      second = line_list[1]
      minute = line_list[2]
      hour = line_list[3]
      day = line_list[4]
      month = line_list[5]
      year = line_list[6]
      year = year.rstrip()
      
      # creates date format
      last_date = hour + ":"  + minute + ":" + second + ", " + day + "-" + month + "-" + year 
      return last_date
