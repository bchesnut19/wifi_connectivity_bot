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
	Set up how often the Summary is tweeted with
in config/config_file.txt, with the value specified
in days. Crontab runs are created using the
initial-setup/initial_config script.

*******************************
*EXPLANATION OF CRONTAB LINES:*
*******************************
After running the initial-setup/initial_config script,
the following lines are added to crontab. X values
will be replaced by values input during initial_config
run.

Causes a general run every X minutes:
*/X * * * * cd /BASE/DIR/ && ./wifiConnBot_run.py 1

Causes a summary tweet every X day of the week:
0 12 * * X cd /BASE/DIR/ && ./wifiConnBot_run.py 0


**********************************
*PLANS(*=critical functionality):*
**********************************
-FINISH TRANSITION TO PYTHON**
-Fix tweet_date_formatter for when only one unit is
 tweeted, WROTE, NEED TO TEST *
-Test to make sure bot functions properly when wifi 
 actually goes down*
-Add to setup script to allow user to set up config
 through command line*
-Add percentage for summary
-Add new documentation
