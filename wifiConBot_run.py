#!/usr/bin/python

##########################################################################
# Description:                                                           #
# Main script for bot, determines whether network interfaces are online  #
# Writes to log files information needed, and calls tweet script to deal #
# with what it should do when wifi goes down.                            #
##########################################################################

# packages needed
import socket
import fcntl
import struct
import os
import sys
import subprocess
import ConfigParser
from time import localtime, strftime

# imported other python files
import interface_csv_status
import tweet


config_file = "config/config_file.txt"
config_reader = ConfigParser.ConfigParser()
config_reader.read(config_file)

#GLOBAL VARS:
#############
LOG_FILE = open("record-keeping/log_file.txt","a+")
ETHER_CSV = open("record-keeping/up_down_eth.csv","a+")
WIFI_CSV = open("record-keeping/up_down_wifi.csv","a+")
# defines script paths
dateCall = "shell-helpers/return_last_date"
timeDownCall = "shell-helpers/calculate_minutes"

# defining names of wifi and eth from config file
ETHER_INTER = config_reader.get('internet-settings', 'ethernet_interface')
WIFI_INTER = config_reader.get('internet-settings', 'wifi_interface')
WIFI_NAME = config_reader.get('internet-settings', 'wifi_network_name')

# time constants
MINUTES_HOUR = 60
MINUTES_DAY = 1440
MINUTES_WEEK = 10080
summary = int(sys.argv[1])

#FUNCTIONS:
###########

# Description: Checks if wifi is down upon start of script, if so restarts
# wifi interface.
def wifi_restart_check():
   wifi_status = interface_csv_status.get_interface_status(False)
   if wifi_status == "OFFLINE":
      down_call = "/sbin/ifdown " + WIFI_NAME
      os.system(down_call)
      up_call = "/sbin/ifup " + WIFI_NAME
      os.system(up_call)
      to_write = strftime("%H:%M%S %m-%d-%Y",localtime())
      to_write = to_write+": "+"Wifi interface restarted\n"
      LOG_FILE.write(to_write)
      return True
   else:
      return False

# Description: finds network status on interface
# Args: hardware = name of hardware interface, etherbool = int serving as
# boolean indicating if interface is ethernet or wifi
# Function Calls: calls check_site_helper, and check_conn_helper
# Writes: LOG_FILE
# Returns: int, 0 indicates connectivity on interface successful,
# 1 indicates connectivity on interface unsuccessful
def check_connectivity_status(hardware,ether_bool):
   google_bool = check_site_helper(hardware, 'google.com')
   bing_bool = check_site_helper(hardware,'bing.com')
   face_bool = check_site_helper(hardware,'facebook.com')
   if google_bool == True or bing_bool == True or face_bool == True:
      to_write = strftime("%H:%M:%S %m-%d-%Y",localtime()) + ": " + hardware + " is active\n"
      LOG_FILE.write(to_write)
      # calls helper with bool for device and device status
      check_conn_helper(True,ether_bool)
      return True
   else:
      to_write= strftime("%H:%M:%S %m-%d-%Y",localtime()) + ": " + hardware + " is down\n"
      LOG_FILE.write(to_write)
      # calls helper with bool for device and device status
      check_conn_helper(False,ether_bool)
      return False

# Description: helper which deals shell calls and writing to logs
# Args: etherbool = int serving as boolean indicating if interface is eth or
# wifi, connBool = int serving as boolean indicating interface connectivity
# status
# Writes: ETHER_CSV, WIFI_CSV
def check_conn_helper(conn_bool,ether_bool):
   to_write=strftime("%S,%M,%H,%d,%m,%Y",localtime())
   current_status = last_status.get_status(ether_bool)
   if current_status == "ONLINE" and conn_bool == True:
      write = False
   elif current_status == "OFFLINE" and conn_bool == False:
      write = False
   else:
      write = True

   if write == True:
      if ether_bool==True:
         to_write=current_status+to_write+"\n"
         ETHER_CSV.write(to_write)
      else:
         to_write=current_status+to_write+"\n"
         WIFI_CSV.write(to_write)

# Description: check interface helper, attempts to connect to site using
# input interface
# Args: hardware = name of interface being used, address = web address
# that connection is attempted on
# Writes: LOG_FILE
def check_site_helper(hardware,address):
   # creates socket used
   sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
   # sets sets socket to use hardware arg
   sock.setsockopt(socket.SOL_SOCKET, 25, hardware)
   sock.settimeout(1)
   # attempts to connect to input web address
   try: 
      sock.connect((address, 80))
      sock.shutdown(socket.SHUT_RDWR)
      sock.close()
      return True
   # if connection failed, writes to log file and returns 1
   except socket.error as err:
      to_write= strftime("%H:%M:%S %m-%d-%Y",localtime())+": " + "Error with " +hardware + " in attempting to access " + address + "\n"
      LOG_FILE.write(to_write)
      return False
def tweet_handler():
   # get last line of wifi csv file
   # if over a certain value
   twitter_destination = config_reader.get('tweeting-info', 'twitter_destination') 
   downTime = subprocess.check_output([dateCall], shell=True)
   tweet_interval = config_reader.get('tweeting-info', 'tweet_interval')
   target_threshold = config_reader.get('tweeting-info', 'tweet_threshold')
   minutesDown = subprocess.check_output([timeDownCall], shell=True)
   minutesDown = int(minutesDown)
   to_write= strftime("%H:%M:%S %m-%d-%Y",localtime())+": "+"Sent Tweet"+ "\n"
   
   if minutesDown == 1:
      tweet_str = "Wifi has gone down at " + downTime
      tweet.send_tweet(tweet_str)
      LOG_FILE.write(to_write)
   elif minutesDown % tweet_interval == 0:
      week_str = units_tweet_helper(minutesDown, MINUTES_WEEK, "week")
      weeks = minutes_unit_calc(minutesDown, MINUTES_WEEK)
      difference = weeks * MINUTES_WEEK
      minutes_diff = minutesDown - difference
      
      day_str = units_tweet_helper(minutes_diff, MINUTES_DAY, "day")
      days = minutes_unit_calc(minutes_diff, MINUTES_DAY)
      difference = days * MINUTES_DAY
      minutes_diff = minutes_diff-difference   

      hour_str = units_tweet_helper(minutes_diff, MINUTES_HOUR, "hour")
      hours = minutes_unit_calc(minutes_diff, MINUTES_HOUR)
      difference = hours * MINUTES_HOUR
      minutes_diff = minutes_diff-difference

      minute_str = units_tweet_helper(minutes_diff,1,"minute")
      minutes = minutes_unit_calc(minutes_diff,1)
         
      tweet_date = tweet_date_formatter(week_str,day_str,hour_str,minute_str,down_time)
      if minutesDown < target_threshold:
         tweet_str = tweet_date
      else:
         tweet_str = twitter_destination + ", " + tweet_date
      tweet.send_tweet(tweet_str)
      LOG_FILE.write(to_write)

def tweet_date_formatter(week_str,day_str,hour_str,minute_str,down_time):
   counter=0
   if week_str! = "":
      counter = counter + 1
   if day_str! = "":
      counter = counter + 1
   if hour_str! = "":
      counter = counter + 1
   if minute_str! = "":
      counter = counter + 1
   if counter > 1:
      and_str = " and"
   else:
      and_str = ""
   
   if minute_str != "":   
      tweet_date = "Wifi has been down for" + week_str + day_str + hour_str + and_str + minute_str + " since: " + down_time
   elif hour_str != "": 
      tweet_date = "Wifi has been down for" + week_str + day_str + and_str + hour_str + " since: " + down_time
   elif day_str! = "":
      tweet_date = "Wifi has been down for" + week_str + and_str + day_str + " since: " + down_time
   else:
      tweet_date = "Wifi has been down for"+week_str+" since: "+down_time
   return tweet_date
   
def minutes_unit_calc(minutes_down, in_unit):
   num_units = 0
   if minutes_down == in_unit:
      num_units = 1
   elif minutes_down < in_unit:
      num_units = 0
   else:
      num_units = minutes_down / in_unit
   return num_units

def units_tweet_helper(minutes_down,in_unit,unit_name):
   num_units = 0
   if (minutes_down / in_unit) == 1:
      tweet_unit = " one " + unit_name + ","
   elif minutes_down < in_unit:
      tweet_unit = ""
   else:
      num_units = minutes_down / in_unit
      tweet_unit = " " + str(num_units) + " " + unit_name + "s,"   
   return tweet_unit

def summary_tweet():
   summary_interval = config_reader.get('tweeting-info', 'wrapup_frequency')

   to_write = strftime("%H:%M:%S %m-%d-%Y",localtime()) + ": " + "Sent Tweet" + "\n"

   summary_call = "shell-helpers/num_times_down " + summary_interval
   num_times_down = subprocess.check_output([summary_call], shell=True)
   tweet_str = "Wifi has gone down " + str(num_times_down) + " times in the last " + str(summary_interval) + " days."
   tweet.send_tweet(tweet_str)
   LOG_FILE.write(to_write)

#######
#MAIN:#
#######

# if wifi was down as of last run, restart wifi interface
wifi_restart_check()
  
# checks connectivity of ether
ether_bool = check_connectivity_status(ETHER_INTER, True)

# checks wifi connectivity
wifi_bool = check_connectivity_status(WIFI_INTER, False)


# Writing results of tests to log file
if ether_bool == True and wifi_bool == True:
   to_write = strftime("%H:%M:%S %m-%d-%Y", localtime())+": CONNECTIONS UP\n"
   LOG_FILE.write(to_write)
else:
   to_write = strftime("%H:%M:%S %m-%d-%Y", localtime())+": "+"NETWORK FAILURES DETECTED\n"
   LOG_FILE.write(to_write)

# calculates time period of downtime of wifi, if over certain length, calls tweet script
# commented out the boolEther check for testing
if wifi_bool == False: #and ether_bool == True:
   tweet_handler()

# need to find way to calculate whether summary should be tweeted
if summary == 0 and ether_bool == True:
   summary_tweet()
