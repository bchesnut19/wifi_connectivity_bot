#!/usr/bin/python
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

# gets ip for interface
def get_ip_address(ifname):
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   return socket.inet_ntoa(fcntl.ioctl(
      s.fileno(),
      0x8915,
      struct.pack('256s', ifname[:15])
   )[20:24])

# network up status, accepts hardware item used as arg
def check_connectivity_status(hardware,etherBool):
   googleBool=check_site_helper(hardware, 'google.com')
   bingBool=check_site_helper(hardware,'bing.com')
   faceBool=check_site_helper(hardware,'facebook.com')
   if googleBool==0 or bingBool==0 or faceBool==0:
      toWrite= "\n"+strftime("%H:%M:%S %m-%d-%y",gmtime())+": "+hardware+" is active"
      logFile.write(toWrite)
      if etherBool==0:
         matchesStatus = subprocess.check_output(["/usr/local/projects/wifi_connectivity_bot/shell-helpers/current_eth_status 0"], shell=True)
         if matchesStatus=="1":
            toWrite = "\nONLINE,"+strftime("%S,%M,%H,%d,%m,%y",gmtime())
            etherCSV.write(toWrite)
      else:
         matchesStatus = subprocess.check_output(["/usr/local/projects/wifi_connectivity_bot/shell-helpers/current_wifi_status 0"], shell=True)
         if matchesStatus=="1":
            toWrite="\nONLINE,"+strftime("%S,%M,%H,%d,%m,%y",gmtime())
            wifiCSV.write(toWrite)
      return 0
   else:
      toWrite= "\n"+strftime("%H:%M:%S %m-%d-%y",gmtime())+": "+hardware+" is down"
      logFile.write(toWrite)
      if etherBool==0:
         matchesStatus = subprocess.check_output(["/usr/local/projects/wifi_connectivity_bot/shell-helpers/current_eth_status 1"], shell=True)
         if matchesStatus=="1":
            toWrite = "\nOFFLINE,"+strftime("%S,%M,%H,%d,%m,%y",gmtime())
            etherCSV.write(toWrite)
      else:
         matchesStatus = subprocess.check_output(["/usr/local/projects/wifi_connectivity_bot/shell-helpers/current_wifi_status 1"], shell=True)
         if matchesStatus=="1":
            toWrite = "\nOFFLINE,"+strftime("%S,%M,%H,%d,%m,%y",gmtime())
            wifiCSV.write(toWrite)
      return 1

# check ethernet helper, accepts hostname addresses
def check_site_helper(hardware,address):
   sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
   # sets hardware device to be used in verifying connection
   sock.setsockopt(socket.SOL_SOCKET, 25, hardware)
   try:
      # attempts to connect to input address with 
      sock.connect((address, 80))
      toWrite= "\n" +strftime("%H:%M:%S %m-%d-%y",gmtime())+": "+"Connected to "+address+" using " +hardware
      logFile.write(toWrite)
      return 0
   except socket.error as err:
      toWrite= "\n"+strftime("%H:%M:%S %m-%d-%y",gmtime())+": " + "Error with " +hardware + " in attempting to access " + address
      logFile.write(toWrite)
      return 1 

#MAIN:
######

ether='eth0'
wifi='wlan0'
# system calls to close internet interfaces are necessary, or else stalls when attempting
# to do connectivity checks on second interface checked
os.system("/sbin/ifdown HTHomeId > /dev/null")
boolEther= check_connectivity_status(ether,0)
os.system("/sbin/ifup HTHomeId > /dev/null")
os.system("/sbin/ifdown eth0 >/dev/null")
boolWifi= check_connectivity_status(wifi,1)
os.system("/sbin/ifup eth0 > /dev/null")
if boolEther==0 and boolWifi==0:
   toWrite = "\n" + strftime("%H:%M:%S %m-%d-%Y", gmtime())+": "+" CONNECTIONS UP"
   logFile.write(toWrite)
else:
   toWrite = "\n"+ strftime("%H:%M:%S %m-%d-%Y", gmtime())+": "+" NETWORK FAILURES DETECTED"
   logFile.write(toWrite)
