#!/bin/python

import sys
import date_functions

# sets the path to the csv file in which wifi down data
# is stored
WIFI_CSV = open('/usr/local/projects/wifi_connectivity_bot/Record_Keeping/up_down_wifi.csv', "r")



def num_downs(interval_minutes):
   read_in = WIFI_CSV.readlines()[2:]
   counter = 0
   for line in read_in:
      date = date_functions.return_date(line)
      minutes_diff = date_functions.calculate_minutes(date)
      line_list = line.split(",")
      if line_list[0] == "OFFLINE" and minutes_diff < interval_minutes: 
         counter += 1
   return counter 
