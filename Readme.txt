README FOR WIFI CONNECTIVITY BOT:
bchesnut19, 07/15/2018

Script begins with checking of the two interfaces on
Raspberry Pi B+, and attempts to connect to different
websites in order to verify connectivity. If any 
websites can be contacted through the interface, the
interface is determined to be online.
	Status information is currently recorded in
csv files located in record-keeping/ dir. The python
script uses a bash helper function for simple data
processing, which allows the program to see if state
of interface has changed since last runtime.

PLANS:
-More through log functionality
-Attempting to remove bash calls
-Add functionality to update webpage with log files
-Add tweet functionality
-Better encorporate config file functionality
