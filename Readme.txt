README FOR WIFI CONNECTIVITY BOT:
bchesnut19, 07/15/2018

Written on Raspberry Pi 3B+ with centOS 7
Should work on any Linux system with Wifi+Ethernet.

DESCRIPTION:
This is a networking monitoring script which is desi-
gned to be run at a frequent interval within crontab.
The script records network log data, and is intended
to be used to harrass your IT department on Twitter.

SETUP FOR SCRIPT RUN:
Within Linux, the default settings do not support
multiple internet connections simultaneously. So in
order for the script to run, kernel variables need to
be changed, which can be done through the use of the
"initial-setup/kernel_network_config" shell script.
This script only needs to be run once, and then it
will trigger a system reboot, applying var changes.
	 Setting up of Twitter API keys and Twitter
target, along with wifi and ethernet name values is
set within config/config_file.txt

EXAMPLE CRONTAB RUN:
Enter crontab using "crontab -e" as root. Enter the
following line:
*/1 * * * * cd /SCRIPT/DIR/ && ./wifiConnBot_run.py
Script will run every minute in correct directory.

SCRIPT BREAKDOWN:
Script begins with checking of the two interfaces on
specified in config_file, and attempts to connect to
different websites in order to verify connectivity. 
If any websites can be contacted through the interfa
-ce, the interface is determined to be online.
	Status information is currently recorded in
csv files located in record-keeping/ dir. The python
script uses a bash helper function for simple data
processing, which allows the program to see if state
of interface has changed since last runtime.
	All processes performed by script are docume-
nted in record-keeping/log_file.txt, along with time
stamps of when operation occured. Errors are written
to logfile as well.
	Calls tweet_script.py in order to send tweet.
This is file where API Keys are stored.
	If wifi down upon last script call, restarts
wifi interface.

PLANS(*=critical functionality):
-Write time comparison for current time and recorded 
 csv downtime*
-Add string arg to tweet_script.py*
-Add functionality to update webpage with log files*
-Try to get script to record logfile times in local time
-Attempting to remove bash script calls (probably more
 trouble than its worth)
