#!/usr/bin/python
# packages needed
import socket
import fcntl
import struct
import os
import subprocess
import time

#GLOBAL VARS:
#############
configFile = open("config_file.txt","r")
logFile = open("record-keeping/log_file.txt","a+")
etherCSV = open("record-keeping/up_down_eth.csv","a+")
wifiCSV = open("record-keeping/up_down_wifi.csv","a+")

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
      print hardware,"is currently active."
      if etherBool==0:
         updateCSV = subprocess.check_output(["./shell-helpers/current_eth_status 0"], shell=True)
         print updateCSV
         if updateCSV=="1":
            global etherCSV
            #timeValue = time.localtime()
            toWrite = "ONLINE,"+"1"
            etherCSV.write(toWrite)
      else:
         updateCSV = subprocess.check_output(["./shell-helpers/current_wifi_status 0"], shell=True)
         print updateCSV
         if updateCSV=="1":
            global wifiCSV
            #timeValue = time.localtime()
            toWrite="ONLINE,"+"1"
            wifiCSV.write(toWrite)
      return 0
   else:
      print hardware,"is down"      
      return 1

# check ethernet helper, accepts hostname addresses
def check_site_helper(hardware,address):
   sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
   # sets hardware device to be used in verifying connection
   sock.setsockopt(socket.SOL_SOCKET, 25, hardware)
   try:
      # attempts to connect to input address with 
      sock.connect((address, 80))
      print "Connected to",address,"using",hardware
      return 0
   except socket.error as err:
      print "Error with:",hardware,"in attempting to access:",address
      return 1 

#MAIN:
######

ether='eth0'
print get_ip_address("eth0")
wifi='wlan0'
os.system("ifdown HTHomeId > /dev/null")
boolEther= check_connectivity_status(ether,0)
os.system("ifup HTHomeId > /dev/null")
os.system("ifdown eth0 >/dev/null")
boolWifi= check_connectivity_status(wifi,1)
os.system("ifup eth0 > /dev/null")
