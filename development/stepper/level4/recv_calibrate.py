#!/usr/bin/env python2

'''
Python wrapper program to calibrate the quantum / polarisation
signal transmission (for sender).
Author: Qcumber 2018
'''

import serial
import sys
import time
import numpy as np

# Parameters
sender_seq = '0123012301230123'

# Obtain device location
devloc_file = 'recv_devloc.txt'
with open(devloc_file) as f:
    content = f.readlines()
serial_addr = content[0][:-1]

# Other parameters declarations
baudrate = 9600      # Default in Arduino
timeout = 0.1        # Serial timeout (in s).

# Starts the program
print "Polarisation Calibrator (Receiver)"
print "Uploading sequence to Arduino..."

# Opens the sender side serial port
receiver = serial.Serial(serial_addr, baudrate, timeout=timeout)

# Send the sequence
receiver.write('POLSEQ ' + sender_seq)

# Block until receive reply
while True:
    if receiver.in_waiting:
        print receiver.readlines()[0] # Should display OK
        break

# Run the sequence
print "Listen for incoming signal..."
receiver.write('RXSEQ ')

# Block until receive 1st reply
while True:
    if receiver.in_waiting:
        res_str = receiver.readlines()[0] # Should display lots of nonsense
        resA = np.array(res_str.split()).astype(np.int)
        print "Measurement done"
        print " "
        break

# Printing cosmetics
print "                    Receiver         "
print "           |  H  |  V  |  D  |  A  | "
print "       | H | " + str(resA[0]).rjust(3,' ') + " | " + str(resA[1]).rjust(3,' ') + " | " + str(resA[2]).rjust(3,' ') + " | "+ str(resA[3]).rjust(3,' ') + " | "
print "Sender | D | " + str(resA[4]).rjust(3,' ') + " | " + str(resA[5]).rjust(3,' ') + " | " + str(resA[6]).rjust(3,' ') + " | "+ str(resA[7]).rjust(3,' ') + " | "
print "       | V | " + str(resA[8]).rjust(3,' ') + " | " + str(resA[9]).rjust(3,' ') + " | " + str(resA[10]).rjust(3,' ') + " | "+ str(resA[11]).rjust(3,' ') + " | "
print "       | A | " + str(resA[12]).rjust(3,' ') + " | " + str(resA[13]).rjust(3,' ') + " | " + str(resA[14]).rjust(3,' ') + " | "+ str(resA[15]).rjust(3,' ') + " | "
print " "

# Calculating the mean
mean = np.average(resA)
print "  The mean is " + str(round(mean, 3))

# Construct the result array-ish
norm_fac = 2 * mean
theoA = norm_fac*np.array([1, 0.5, 0, 0.5, 0.5, 1, 0.5, 0, 0, 0.5, 1, 0.5, 0.5, 0, 0.5, 1])
delta = np.abs(theoA-resA)
deviation = np.sum(delta) / (16 * mean)
print "  Signal degradation is " + str(round(deviation, 3))
print "  "

# Print last statement and exits the program
