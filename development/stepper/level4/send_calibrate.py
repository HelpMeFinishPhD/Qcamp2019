#!/usr/bin/env python2

'''
Python wrapper program to calibrate the quantum / polarisation
signal transmission (for sender).
Author: Qcumber 2018
'''

import serial
import sys
import time

# Parameters
sender_seq = '0000111122223333'

# Obtain device location
devloc_file = 'send_devloc.txt'
with open(devloc_file) as f:
    content = f.readlines()
serial_addr = content[0][:-1]

# Other parameters declarations
baudrate = 9600      # Default in Arduino
timeout = 0.1        # Serial timeout (in s).

# Starts the program
print "Polarisation Calibrator (Sender)"
print "Uploading sequence to Arduino..."

# Opens the sender side serial port
sender = serial.Serial(serial_addr, baudrate, timeout=timeout)

# Send the sequence
sender.write('POLSEQ ' + sender_seq)

# Block until receive reply
while True:
    if sender.in_waiting:
        print sender.readlines()[0] # Should display OK
        break

# Run the sequence
print "Running the sequence..."
sender.write('TXSEQ ')

# Block until receive reply
while True:
    if sender.in_waiting:
        print sender.readlines()[0] # Should display OK
        break

# Print last statement and exits the program
print "Task done. Look at Receiver for the calibration result"
