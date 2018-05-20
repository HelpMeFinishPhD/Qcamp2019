#!/usr/bin/env python2

'''
Python wrapper program to send a sequence of 16 bit keys (Alice)
without key sifting (it will be done manually).
Author: Qcumber 2018
'''

import serial
import sys
import time

# Function to convert to hex, with a predefined nbits
def tohex(val, nbits):
  return hex((val + (1 << nbits)) % (1 << nbits))

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
print "Alice, Are you ready? This is the key sender program."
print "Randomising key bits and basis bits using Arduino"

# Randomising the sequence
sender.write('RNDSEQ ')

# Block until receive reply
while True:
    if sender.in_waiting:
        print sender.readlines()[0] # Should display OK
        break

print "Arduino says he/she likes to choose the following bits:"

# Find out what is the key
sender.write('SEQ? ')

# Block until receive 1st reply
while True:
    if sender.in_waiting:
        reply_str = sender.readlines()[0][:-1] # Remove the /n
        break

print reply_str
# Obtain the binary string repr for val and bas bits
val_str = ""
bas_str = ""
for bit in reply_str:
    val_str += str(int(bit) // 2)
    bas_str += str(int(bit) % 2)

print val_str
print int("0b"+val_str, 0)
print tohex(int("0b"+val_str, 0), 16)
print bas_str

# Giving the reply in HEX format
val_hex = tohex(int("0b"+val_str, 0), 16) # Get int, and convert to 16 bit hex
bas_hex = tohex(int("0b"+bas_str, 0), 16) # Get int, and convert to 16 bit hex
print "Value bits (in hex):", val_hex[2:].zfill(4)
print "Basis bits (in hex):", bas_hex[2:].zfill(4)

# Run the sequence
print "\nRunning the sequence..."
sender.write('TXSEQ ')

# Block until receive reply
while True:
    if sender.in_waiting:
        print sender.readlines()[0] # Should display OK
        break

# Print last statement and exits the program
print "Task done. Please perform key sifting with Bob via public channel."
