#!/usr/bin/env python2

'''
Python wrapper program to send 32 bits QKD keys via
quantum and classial channel
Author: Qcumber 2018
'''

import serial
import sys
import time

''' Helper functions '''

def send4BytesC(message_str):
    if len(message_str) == 4:
        deviceC.write('SEND ') # Flag to send
        deviceC.write(message_str)
    else:
        print "The message is not 4 bytes. Please check again"

def recv4BytesC():
    deviceC.write('RECV ') # Flag to recv
    while True:            # Block until receives a reply
        if deviceC.in_waiting:
            hex_string = deviceC.read(8)
            break
    # Convert to ASCII string
    hex_list= map(''.join, zip(*[iter(hex_string)]*2))
    ascii_string = "".join([chr(int("0x"+each_hex,0)) for each_hex in hex_list])
    return ascii_string

# Obtain device location
devloc_fileC = 'devloc_classical.txt'
devloc_fileQ = 'devloc_quantum.txt'
with open(devloc_fileC) as f:
    contentC = f.readlines()
serial_addrC = contentC[0][:-1]
with open(devloc_fileQ) as f:
    contentQ = f.readlines()
serial_addrQ = contentQ[0][:-1]

# Other parameters declarations
baudrate = 9600      # Default in Arduino
rep_wait_time = 1    # 1 s wait time between each tries
timeout = 0.1        # Serial timeout (in s).

# Opens the sender side serial port
deviceC = serial.Serial(serial_addrC, baudrate, timeout=timeout)
deviceQ = serial.Serial(serial_addrQ, baudrate, timeout=timeout)

print "Here we go"

try:
    send4BytesC("HELL")
    print recv4BytesC()
except KeyboardInterrupt:
    # End of program
    deviceC.write('#') # Flag to force end listening
    print ("\nProgram interrupted. Thank you for using the program!")
    sys.exit()  # Exits the program
