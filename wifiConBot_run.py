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
from time import localtime, strftime

#GLOBAL VARS:
#############
logFile = open("record-keeping/log_file.txt","a+")
etherCSV = open("record-keeping/up_down_eth.csv","a+")
wifiCSV = open("record-keeping/up_down_wifi.csv","a+")
# defines script paths
dateCall = "shell-helpers/return_last_date"
config = "config/config_reader"
check_conn = "shell-helpers/interface_csv_status"
timeDownCall = "shell-helpers/calculate_minutes"
# defining names of wifi and eth from config file
etherCall = config+" 3"
ether = subprocess.check_output([etherCall], shell=True) 
wifiIntCall = config+" 1"
wifiInter = subprocess.check_output([wifiIntCall], shell=True)
wifiNameCall = config+" 2"
wifiName = subprocess.check_output([wifiNameCall], shell=True)
hourMinutes = 60
dayMinutes = 1440
weekMinutes = 10800


#FUNCTIONS:
###########

# Description: Checks if wifi is down upon start of script, if so restarts
# wifi interface.
def wifi_restart_check():
   scriptCall = check_conn+" 1"+" 1"
   wifiDown = subprocess.check_output([scriptCall], shell=True)
   if wifiDown==0:
      downCall="/sbin/ifdown "+wifiName
      os.system(downCall)
      upCall="/sbin/ifup "+wifiName
      os.system(upCall)
      toWrite=strftime("%H:%M%S %m-%d-%Y",localtime())
      toWrite=toWrite+": "+"Wifi interface restarted\n"
      logFile.write(toWrite)
      return 0
   else:
      return 1

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
      toWrite=strftime("%H:%M:%S %m-%d-%Y",localtime())+": "+hardware+" is active\n"
      logFile.write(toWrite)
      # calls helper with bool for device and device status
      check_conn_helper(etherBool,0)
      return 0
   else:
      toWrite= strftime("%H:%M:%S %m-%d-%Y",localtime())+": "+hardware+" is down\n"
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
   toWrite=strftime("%S,%M,%H,%d,%m,%Y",localtime())
   scriptCall=check_conn+" "+str(connBool)+" "+str(etherBool)
   if etherBool==0:
      matchesStatus = subprocess.check_output([scriptCall], shell=True)
   else:
      matchesStatus = subprocess.check_output([scriptCall], shell=True)
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
            toWrite="OFFLINE,"+toWrite+"\n"
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
   sock.settimeout(1)
   # attempts to connect to input web address
   try: 
      sock.connect((address, 80))
      sock.shutdown(socket.SHUT_RDWR)
      sock.close()
      return 0
   # if connection failed, writes to log file and returns 1
   except socket.error as err:
      toWrite= strftime("%H:%M:%S %m-%d-%Y",localtime())+": " + "Error with " +hardware + " in attempting to access " + address + "\n"
      logFile.write(toWrite)
      return 1
def tweet_handler():
   # get last line of wifi csv file
   # if over a certain value
   twitterCall = config+" 4"
   tweetInterval = int(config+" 9")
   targetThreshold = int(config+" 10")
   twitterDestination = subprocess.check_output([twitterCall], shell=True)
   downTime = subprocess.check_output([dateCall], shell=True)
   minutesDown = subprocess.check_output([timeDownCall], shell=True)
   minutesDown = int(minutesDown)
   toWrite= strftime("%H:%M:%S %m-%d-%Y",localtime())+": "+"Sent Tweet"+ "\n"
   
   if minutesDown%tweetInterval==0:
      weeks = units_tweet_helper(minutesDown,minutesWeek)
      if weeks==1:
         weekStr=" one week, "
      elif weeks>1:
         weekStr=" "+str(weeks)+ " weeks, "
      else:
         weekStr=""
      difference=weeks*minutesWeek
      minutesDiff=minutesDiff-difference      
      
      days = units_tweet_helper(minutesDiff,minutesDay)
      if days==1:
         dayStr=" one day, "
      elif days>1:
         dayStr=" "+str(days)+" days, "
      else:
         dayStr=""
      difference=days*minutesDay
      minutesDiff=minutesDiff-difference   

      hours = units_tweet_helper(minutesDiff,minutesHour)
      if hours==1:
         hourStr=" one hour, "
      elif hours>1:
         hourStr=" "+str(hours)+" hours, "
      else:
         hourStr=""
      difference=hours*minutesHour
      minutesDiff=minutesDiff-difference
      
      if minutesDiff==1:
         minuteStr = " one minute, "
      elif minutesDiff>1:
         minutesStr=" "+str(minutesDiff)+" minutes, "
      else:
         minutesStr=""

      if minutesDiff==1:
         tweet="Wifi has gone down at "+downTime
         tweetCall = "./tweet_script.py "+"\""+tweet+"\""
         os.system(tweetCall)
         logFile.write(toWrite)
      elif minutesDown<targetThreshold:
         tweet="Wifi has been down for"+weekStr+dayString+hourStr+minuteStr+"since: "+downTime
         tweetCall = "./tweet_script.py "+"\""+tweet+"\""
         os.system(tweetCall)
         logFile.write(toWrite)
      else:
         tweet=twitterDestination + ", Wifi has been down for "+weekStr+dayStr+hourStr+minuteStr+"since: "+downTime
         tweetCall = "./tweet_script.py " +"\""+tweet+"\""
         os.system(tweetCall)
         logFile.write(toWrite)

def units_tweet_helper(minutesDown,inUnit):
   if minutesDown==inUnit:
      return 1
   elif minutesDown<inUnit:
      return 0
   else:
      numUnit=0
      while (numMinutes>inUnit):
         numMinutes = numMinutes-inUnit
         numUnit=numUnit+1
      return numUnit
      

#######
#MAIN:#
#######

# if wifi was down as of last run, restart wifi interface
wifi_restart_check()
  
# checks connectivity of ether
boolEther= check_connectivity_status(ether,0)

# checks wifi connectivity
boolWifi= check_connectivity_status(wifiInter,1)

# Writing results of tests to log file
if boolEther==0 and boolWifi==0:
   toWrite = strftime("%H:%M:%S %m-%d-%Y", localtime())+": CONNECTIONS UP\n"
   logFile.write(toWrite)
else:
   toWrite = strftime("%H:%M:%S %m-%d-%Y", localtime())+": "+"NETWORK FAILURES DETECTED\n"
   logFile.write(toWrite)

# calculates time period of downtime of wifi, if over certain length, calls tweet script
if boolWifi==1:
   # get last line of wifi csv file
   # if over a certain value
   tweet_handler()
