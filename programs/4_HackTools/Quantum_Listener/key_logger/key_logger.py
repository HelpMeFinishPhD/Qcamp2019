#!/usr/bin/env python2

'''
Python wrapper program to log the measurement result for Eve
This version will log from two devices: Arduino (serial1) and powermeter (serial2)
Author: Qcumber 2018
'''

import serial
import sys
import time
import datetime

# Serial 1
serial_addr1 = '/dev/ttyACM0'   # Arduino

# Serial 2
serial_addr2 = '/dev/ttyACM1'   # Powermeter

print "The JW Eavesdropping... will record any voltages into a file"
print "To exit the program, use Ctrl+C \n"

# Other parameters declarations

# Serial 1
baudrate1 = 9600      # Default in Arduino
timeout1 = 0.1        # Serial timeout (in s).
refresh_rate= 0.0     # Minimum offset around 115 ms

# Serial 2
baudrate2 = 115200    # Default in Arduino
timeout2 = 0          # Serial timeout (in s).
# Some note (may be a bug in the future):
# The pyserial somehow does not properly respond to powermeter timeout
# I will just assume it to have 0 timeout, and let the blocking donw
# by the other device's response time.

# Opens the receiver side serial port
receiver1 = serial.Serial(serial_addr1, baudrate1, timeout=timeout1)
receiver2 = serial.Serial(serial_addr2, timeout=timeout2)

# Waiting until the serial device is open (for some computer models)
time.sleep(2)
print "Ready!\n"

# Setting the range for powermeter
receiver2.write("RANGE3\n")

# The filename is the current time
filename =  str(datetime.datetime.now().time())[:8] + '.dat'
print "Logging the voltages into:", filename

while True:
    try:
        receiver1.write("VOLT? ")
        receiver2.write("VOLT?\n")

        # Block until receive the reply
        while True:
            if receiver1.in_waiting:
                volt_now1 = receiver1.readlines()[0][:-2] # Remove the /n
                volt_now2 = receiver2.readlines()[0][1:-2] # Remove the /n
                break
        print volt_now1, volt_now2
        # Write to a file
        with open(filename, "a") as myfile:
            myfile.write(volt_now1 + " " + str(volt_now2) + "\n")
        # Wait until the next time
        time.sleep(refresh_rate)
    except KeyboardInterrupt:
        print ("\nThank you for using the program!")
        sys.exit()  # Exits the program
