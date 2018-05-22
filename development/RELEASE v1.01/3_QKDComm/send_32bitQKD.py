#!/usr/bin/env python2

'''
Python wrapper program to send 32 bits QKD keys via
quantum and classial channel
Author: Qcumber 2018
'''

import serial
import sys
import time

# Parameter
rep_wait_time = 0.3  # Wait time between packets (in s).

''' Helper functions '''

def send4BytesC(message_str):
    if len(message_str) == 4:
        deviceC.write('SEND ') # Send identifier [BEL]x3 + A
        deviceC.write(b'\x07\x07\x07' + 'A') # This is Alice (sender)
        time.sleep(rep_wait_time)
        deviceC.write('SEND ') # Send message
        deviceC.write(message_str)
    else:
        print "The message is not 4 bytes. Please check again"

def recv4BytesC():
    deviceC.write('RECV ') # Flag to recv
    state = 0   # 0: waiting for STX, 1: transmitting/ wait for ETX
    while True: # Block until receives a reply
        if deviceC.in_waiting:
            if hex_string == '7070742':  # 07-[BEL], 42-B (Header from Bob)
                print ("Received message!") # Debug
                state = 1
            elif state == 1:
                hex_string = deviceC.read(8)
                break
    # Convert to ASCII string
    hex_list = map(''.join, zip(*[iter(hex_string)]*2))
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
    send4BytesC("BLAH")
    print recv4BytesC()
    print recv4BytesC()
except KeyboardInterrupt:
    # End of program
    deviceC.write('#') # Flag to force end listening
    print ("\nProgram interrupted. Thank you for using the program!")
    sys.exit()  # Exits the program
