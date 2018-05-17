#!/usr/bin/env python2

'''
Python program to test the randomness of Entropy library
Author: Qcumber 2018
'''

import serial
import sys
import time
import numpy as np

# Obtain device location
devloc_file = 'devloc.txt'
with open(devloc_file) as f:
    content = f.readlines()
serial_addr = content[0][:-1]

# Other parameters declarations
baudrate = 9600      # Default in Arduino
timeout = 0.1        # Serial timeout (in s).

# Opens the sender side serial port
device = serial.Serial(serial_addr, baudrate, timeout=timeout)

start = time.time()
howmany = 1000
i = 0
while True:
    # Send the sequence
    device.write('RNDSEQ ')
    # Block until receive reply
    while True:
        if device.in_waiting:
            device.readlines()[0][:-1]
            break
    # Get the sequence
    device.write('SEQ? ')
    # Block until receive reply
    while True:
        if device.in_waiting:
            string = device.readlines()[0][:-1] # Should display OK
            len_string = len(string)
            number = 0
            for s in range(len_string):
                increment =  int(string[s]) * 4 ** s
                number += increment
            print "NUMBER", number
            with open("numbers.txt", "a") as myfile:
                myfile.write(str(number)+'\n')
            break
    i +=1
    if i >= howmany:
        break

end = time.time()
delta_t = end - start
print "Time has passed", delta_t, "s"
