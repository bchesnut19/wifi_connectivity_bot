#!/bin/python
import csv
import sys

def get_interface_status(file_bool):
   if file_bool == 0:
      csv_file = open('/usr/local/projects/wifi_connectivity_bot/record-keeping/up_down_eth.csv', "r")
   else:
      csv_file = open('/usr/local/projects/wifi_connectivity_bot/record-keeping/up_down_eth.csv', "r")
   
   list_file = csv_file.readlines()
   csv_file.close()
   # grabs final line from input file
   final_line = list_file[len(list_file)-1]
   csv_row = final_line.split(",")
   # grabs the first field from file
   return csv_row[0]  
