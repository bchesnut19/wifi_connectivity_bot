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
import subprocess
from time import gmtime, strftime

#GLOBAL VARS:
#############
configFile = open("/usr/local/projects/wifi_connectivity_bot/config_file.txt","r")
logFile = open("/usr/local/projects/wifi_connectivity_bot/record-keeping/log_file.txt","a+")
etherCSV = open("/usr/local/projects/wifi_connectivity_bot/record-keeping/up_down_eth.csv","a+")
wifiCSV = open("/usr/local/projects/wifi_connectivity_bot/record-keeping/up_down_wifi.csv","a+")

#FUNCTIONS:
###########

# Description: finds network status on interface
# Args: hardware = name of hardware interface, etherbool = int serving as
# boolean indicating if interface is ethernet or wifi
# Function Calls: calls check_site_helper, and check_conn_helper
# Writes: logFile
# Returns: int, 0 indicates connectivity on interface successful,
# 1 indicates connectivity on interface unsuccessful
def check_connectivity_status(hardware,etherBool):
   googleBool=check_site_helper(hardware, 'google.com')
   bingBool=check_site_helper(hardware,'bing.com')
   faceBool=check_site_helper(hardware,'facebook.com')
   if googleBool==0 or bingBool==0 or faceBool==0:
      toWrite=strftime("%H:%M:%S %m-%d-%Y",gmtime())+": "+hardware+" is active\n"
      logFile.write(toWrite)
      # calls helper with bool for device and device status
      check_conn_helper(etherBool,0)
      return 0
   else:
      toWrite= strftime("%H:%M:%S %m-%d-%Y",gmtime())+": "+hardware+" is down\n"
      logFile.write(toWrite)
      # calls helper with bool for device and device status
      check_conn_helper(etherBool,1)
      return 1

# Description: helper which deals shell calls and writing to logs
# Args: etherbool = int serving as boolean indicating if interface is eth or
# wifi, connBool = int serving as boolean indicating interface connectivity
# status
# Writes: etherCSV, wifiCSV
def check_conn_helper(etherBool,connBool):
   toWrite=strftime("%S,%M,%H,%d,%m,%Y")
   scriptCall="/usr/local/projects/wifi_connectivity_bot/shell-helpers/interface_csv_status"
   if etherBool==0:
      matchesStatus = subprocess.check_output([scriptCall," ",str(connBool)," ",str(etherBool)], shell=True)
   else:
      matchesStatus = subprocess.check_output([scriptCall,str(connBool),str(etherBool)], shell=True)
   if matchesStatus=="1":
      if etherBool==0:
         if connBool==0:
            toWrite="ONLINE,"+toWrite+"\n"
            etherCSV.write(toWrite)
         else:
            toWrite="OFFLINE,"+toWrite+"\n"
            etherCSV.write(toWrite)
      else:
         if connBool==0:
            toWrite="ONLINE,"+toWrite+"\n"
            wifiCSV.write(toWrite)
         else:
            toWrite="OFFLINE"+toWrite+"\n"
            wifiCSV.write(toWrite)

# Description: check interface helper, attempts to connect to site using
# input interface
# Args: hardware = name of interface being used, address = web address
# that connection is attempted on
# Writes: logFile
def check_site_helper(hardware,address):
   # creates socket used
   sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
   # sets sets socket to use hardware arg
   sock.setsockopt(socket.SOL_SOCKET, 25, hardware)
   # attempts to connect to input web address
   try: 
      sock.connect((address, 80))
      sock.shutdown(socket.SHUT_RDWR)
      sock.close()
      return 0
   # if connection failed, writes to log file and returns 1
   except socket.error as err:
      toWrite= strftime("%H:%M:%S %m-%d-%Y",gmtime())+": " + "Error with " +hardware + " in attempting to access " + address + "\n"
      logFile.write(toWrite)
      return 1 
#######
#MAIN:#
#######

# CHANGE TO READ INTERFACE NAMES FROM CONFIGFILE/HARDWARE
# defining names of hardware interfaces and code calls 
ether='eth0'
wifiInter='wlan0'

# checks connectivity of ether
boolEther= check_connectivity_status(ether,0)

# checks wifi connectivity
boolWifi= check_connectivity_status(wifiInter,1)

# Writing results of tests to log file
if boolEther==0 and boolWifi==0:
   toWrite = strftime("%H:%M:%S %m-%d-%Y", gmtime())+": CONNECTIONS UP\n"
   logFile.write(toWrite)
else:
   toWrite = strftime("%H:%M:%S %m-%d-%Y", gmtime())+": "+"NETWORK FAILURES DETECTED\n"
   logFile.write(toWrite)

# calculates time period of downtime of wifi, if over certain length, calls tweet script
if boolWifi==0:
   # get last line of wifi csv file
   # if over a certain value
   logFile.write("CALL TWEET SCRIPT\n") 
