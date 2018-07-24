README FOR WIFI CONNECTIVITY BOT:
bchesnut19, 07/15/2018

Written on Raspberry Pi 3B+ with centOS 7
Should work on any Linux system with Wifi+Ethernet.

**************
*DESCRIPTION:*
**************
This is a networking monitoring script which is desi-
gned to be run at a frequent interval within crontab.
The script records network log data, and is intended
to be used to harrass your IT department on Twitter.

****************************
*NON-STANDARD DEPENDENCIES:*
****************************
twitter-api for Python.

***********************
*SETUP FOR SCRIPT RUN:*
***********************
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

**********************
*EXAMPLE CRONTAB RUN:*
**********************
Enter crontab using "crontab -e" as root. Enter the
following line:
*/1 * * * * cd /SCRIPT/DIR/ && ./wifiConnBot_run.py
Script will run every minute in correct directory.

*******************
*SCRIPT BREAKDOWN:*
*******************

*********
*PYTHON:*
*********

wifiConBot_run.py:
******************
Description:
wifiConBot_run.py serves as the primary run script
for the wifi connectivity bot. This script is where
the handling of the status of the network interfaces
occurs.

Imported libraries: socket, fcntl, struct,
os, subprocess, and from time->localtime and srtftime.

Global Variables:
Global variables defined include the file paths for 
the various logfiles written to, along with names of
interfaces and wifi network name. Paths for helper
bash scripts are also defined, along with the twitter
handle that is targeted when extensive downtime occurs.

Logical Flow:
Script begins with calling the function: 
"wifi_restart_check(). This function checks the
recorded status of the wifi interface from the last
run, using the bash script "shell-helper/check_conn"
with args for wifi and down. This is used to deter-
mine if the wifi interface was determined to be down
as of the last run of the main script. If this func
returns true, the wifi interface is restarted in
order to attempt to restablish connectivity.
	Next, the script calls the function
"check_connectivity_status(etherBool,connectedBool)".
Within this function, it attempts to connect to
assorted websites in order to establish if the net-
work interfaces are up or down. This is done through 
the use of "check_site_helper(hardware,site)". Upon
the completed test of connectivity, the status of the
interface is written to its respective CSV file using
"check_conn_helper(etherBool,connectedBool)". This
status is only recorded if the last recorded status in
its CSV file does not match current network status.
	Finally, if the wifi connection is determined
to be down by the check_connectivity_status call, the
"tweet_handler()" function is called. This script uses
the bash scripts "shell-helpers/return_last_date" and 
"shell-helpers/calculate_minutes" in order to determine
the string that will be tweeted using the 
"tweet_script.py" script.
	Throughout the course of the script run, it
writes information of intrest to its logfile in
"record-keeping/log_file.txt". Information recorded
here includes any website connections that failed,
along with whether an interface was determined to be
down, and whether the script sent out a tweet. Log ent-
ries are recorded with local timestamps.
	The secondary Python script is tweet_script.py,
which is the script from which the actual tweet is
sent out using the twitter-api library for Python.
tweet_script.py accepts the string to be tweeted as
an argument, and reads API keys from the config file. 

BASH:
Bash scripts serve as helpers to the primary python
function, wifiConRun_bot.py. 
script uses bash helper scriptss for simple data
processing.
	All processes performed by script are docume-
nted in record-keeping/log_file.txt, along with time
stamps of when operation occured. Errors are written
to logfile as well.
	If wifi down upon last script call, restarts
wifi interface.
	Compares downtime from up_down_wifi.csv with
current time, tweets at 30 minutes of downtime, and
hourly after. Upon two hour mark, begins tweeting at
account specified in logfile.


**********************************
*PLANS(*=critical functionality):*
**********************************
-Add functionality to update webpage with log files*
-Create wiki and transfer some readme info to wiki
-Finish program logic description
-Attempting to remove bash script calls (probably more
 trouble than its worth)
