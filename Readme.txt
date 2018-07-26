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


**********************************
*PLANS(*=critical functionality):*
**********************************
-Add functionality to update webpage with log files*
-Fix tweet_date_formatter for when only one unit is
 tweeted
-Add new documentation for scripts
-Test to make sure bot functions properly when wifi 
 actually goes down.
-Attempting to remove bash script calls (probably more
 trouble than its worth)
