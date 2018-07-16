#!/usr/bin/python
import socket
import fcntl
import struct

#FUNCTIONS:
###########
# sets files used in program
def file_setting():
   configFile = open("config_file.txt","r");
   logFile = open("record-keeping/log_file.txt","w");
   csvFile = open("record-keeping/up_down.csv","w");

#MAIN:
######

file_setting
print("TEST 123")
