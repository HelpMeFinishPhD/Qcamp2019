#!/usr/bin/env python2

'''
Python wrapper program to send a string through the IR channel with
the NEC-string protocol.
Author: Qcumber 2018
'''

import serial
import sys
import time

# Text to send and verify
text = "Qc!8" # Maximum of 4 bytes / 4 characters

# Obtain device location
devloc_file = 'devloc.txt'
with open(devloc_file) as f:
    content = f.readlines()
serial_addr = content[0][:-1]

# Other parameters declarations
baudrate = 9600      # Default in Arduino
rep_wait_time = 1    # 1 s wait time between each tries
timeout = 0.1        # Serial timeout (in s).

# Opens the sender side serial port
sender = serial.Serial(serial_addr, baudrate, timeout=timeout)

while True:
    try:
        print "Trying to send the text:", text
        print "To exit the program, use Ctrl+C\n"
        sender.write('SEND ') # Flag to send
        sender.write(text)    # Sending the text
        time.sleep(rep_wait_time)

    except KeyboardInterrupt:
        print ("\nThank you for using the program!")
        sys.exit()  # Exits the program
