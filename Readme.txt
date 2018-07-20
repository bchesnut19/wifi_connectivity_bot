README FOR WIFI CONNECTIVITY BOT:
bchesnut19, 07/15/2018
centOS 7

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
	All processes performed by script are docume-
nted in record-keeping/log_file.txt, along with time
stamps of when operation occured. Errors are written
to logfile as well.


PLANS(*=critical functionality):
-Find way to get around having to take down interface
 to test connectivity in the other*
-Tracking downtime*
-Add tweet functionality*
-Implement config file*
-Add functionality to update webpage with log files*
-Reading in interface names from either configFile or
 hardware
-Attempting to remove bash script calls
