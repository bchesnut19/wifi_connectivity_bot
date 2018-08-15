#!/usr/bin/python
import twitter
import sys
import subprocess
import socket
import ConfigParser

CONFIG_FILE = "/usr/local/projects/wifi_connectivity_bot/config/config_file.txt"

def send_tweet(tweet_str):
   # reads in values from config file
   config_reader = ConfigParser.ConfigParser()
   config_reader.read(CONFIG_FILE)
   con_key = config_reader.get('twitter-keys', 'consumer_key')
   con_secr = config_reader.get('twitter-keys', 'consumer_secret')
   token_key = config_reader.get('twitter-keys', 'access_token_key')
   token_secr = config_reader.get('twitter-keys', 'access_token_secret')

   ethernet = config_reader.get('internet-settings', 'ethernet_interface')

   # connects to the twitter api through the ethernet interface
   # to prevent screwups.
   port = 443
   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   sock.setsockopt(socket.SOL_SOCKET, 25, ethernet)
   sock.connect(('api.twitter.com',port))


   api = twitter.Api(consumer_key=con_key,
                     consumer_secret=con_secr,
                     access_token_key=token_key, 
                     access_token_secret=token_secr)
   api.PostUpdate(tweet_str)
