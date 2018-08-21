#!/bin/python
import csv
import sys

PATH = None

def init(path):
   global PATH
   PATH = path

def get_status(file_bool):
   if file_bool == True:
      path = PATH + "Record_Keeping/up_down_eth.csv"
      csv_file = open(path, "r")
   else:
      path = PATH + "Record_Keeping/up_down_wifi.csv"
      csv_file = open(path, "r")
   
   list_file = csv_file.readlines()
   csv_file.close()
   # grabs final line from input file
   final_line = list_file[len(list_file)-1]
   csv_row = final_line.split(",")
   # grabs the first field from file
   return csv_row[0]  
