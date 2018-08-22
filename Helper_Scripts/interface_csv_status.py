#!/bin/python
import csv
import sys
from contextlib import contextmanager, closing

def get_status(file_bool):
   if file_bool == True:
      csv_file = '/usr/local/projects/wifi_connectivity_bot/Record_Keeping/up_down_eth.csv'
   else:
      csv_file = '/usr/local/projects/wifi_connectivity_bot/Record_Keeping/up_down_wifi.csv'
   
   with closing( open(csv_file, "r") ) as csv:
      list_file = csv.readlines()
      
   # grabs final line from input file
   final_line = list_file[len(list_file)-1]
   csv_row = final_line.split(",")
   # grabs the first field from file
   return csv_row[0]  
