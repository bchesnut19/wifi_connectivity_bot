#!/usr/bin/python
import twitter
import sys
import subprocess

# SET UP ARGUMENT INPUT FOR TWEET
configReader = "config/config_reader"
conKeyCall = configReader+" 5"
conKey = subprocess.check_output([conKeyCall], shell=True)
conSecrCall = configReader+" 6"
conSecr = subprocess.check_output([conSecrCall], shell=True)
tokeKeyCall = configReader+" 7"
tokeKey = subprocess.check_output([tokeKeyCall], shell=True)
tokeSecrCall = configReader+" 8"
tokeSecr = subprocess.check_output([tokeSecrCall], shell=True)  

api = twitter.Api(consumer_key=conKey, #subprocess.check_output([conKeyCall], shell=True),
                  consumer_secret=conSecr, #subprocess.check_output([conSecrCall, shell=True]),
                  access_token_key=tokeKey, #subprocess.check_output([tokeKeyCall], shell=True),
                  access_token_secret=tokeSecr) #subprocess.check_output([tokeSecrCall], shell=True))
api.PostUpdate("@roastedchesnut test123")
