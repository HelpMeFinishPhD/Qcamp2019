#!/usr/bin/env python2

'''
Python wrapper program to send a sequence of 16 bit keys (Alice)
without key sifting (it will be done manually).
Author: Qcumber 2018
'''

import serial
import sys
import time

# Obtain device location
devloc_file = 'devloc.txt'
with open(devloc_file) as f:
    content = f.readlines()
serial_addr = content[0][:-1]

# Other parameters declarations
baudrate = 9600      # Default in Arduino
timeout = 0.1        # Serial timeout (in s).

# Opens the sender side serial port
sender = serial.Serial(serial_addr, baudrate, timeout=timeout)

# Starts the program
print "Alice, Are you ready? This is key sender"
print "Randomising key bits and basis bits using Arduino"

# Randomising the sequence
sender.write('RNDSEQ ' + sender_seq)



# Rre
print "Running the sequence"


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
