#!/bin/python
###########################################################################
# Description:                                                            #
# Calculates time passed since wifi went down in minutes                  #
###########################################################################

import datetime

def return_date(line_in):

   # reads in a line from csv file which is then turned into a timestamp
   csv_row = line_in.split(",")
   
   second_in = int(csv_row[1])
   minute_in =int(csv_row[2])
   hour_in = int(csv_row[3])
   day_in = int(csv_row[4])
   month_in =int(csv_row[5])
   year_in = csv_row[6]
   year_in = int( year_in.rstrip() )
   
   line_date = datetime.datetime(
               second = second_in, minute = minute_in, hour = hour_in, day = day_in, \
               month = month_in, year = year_in)
   return line_date

def calculate_minutes(date_in):

   current_time = datetime.datetime.now()
   
   # gets total days between two dates
   day_diff = int( abs( (current_time - date_in).days ) )
   # gets difference in second values between two dates
   second_diff = int( abs( (current_time - date_in).seconds ) )
   
   minutes = ( 24 * 60 * day_diff ) + ( second_diff / 60 )
   
   return minutes
  
