#!/usr/bin/env python2

'''
Python wrapper program to log the measurement result for Eve
Author: Qcumber 2018
'''

import serial
import sys
import time
import datetime

print "The JW Eavesdropping... will record any voltages into a file"
print "To exit the program, use Ctrl+C \n"

# Obtain device location
devloc_file = 'devloc.txt'
with open(devloc_file) as f:
    content = f.readlines()
serial_addr = content[0][:-1]

# Other parameters declarations
baudrate = 9600      # Default in Arduino
timeout = 0.1        # Serial timeout (in s).
refresh_rate = 0.0   # Minimum offset around 115 ms

# Opens the receiver side serial port
receiver = serial.Serial(serial_addr, baudrate, timeout=timeout)

# The filename is the current time
filename =  str(datetime.datetime.now().time())[:8] + '.dat'
print "Logging the voltages into:", filename

while True:
    try:
        receiver.write("VOLT? ")
        # Block until receive the reply
        while True:
            if receiver.in_waiting:
                volt_now = receiver.readlines()[0][:-1] # Remove the /n
                break
        print volt_now
        # Write to a file
        with open(filename, "a") as myfile:
            myfile.write(volt_now)
        # Wait until the next time
        time.sleep(refresh_rate)
    except KeyboardInterrupt:
        print ("\nThank you for using the program!")
        sys.exit()  # Exits the program
