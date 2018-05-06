#!/usr/bin/env python2

'''
Python wrapper program to receive a string through the IR channel with
the NEC-string protocol.
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
receiver = serial.Serial(serial_addr, baudrate, timeout=timeout)

while True:
    try:
        msg_string = "\n" +\
                     "NEC-string Protocol Receiver Qcumber v1.00 \n" +\
                     "To exit the program, use Ctrl+C \n" +\
                     "Waiting for data ... \n"
        print(msg_string)
        state = 0 # 0 : waiting for STX, 1 : transmitting/ wait for ETX
        while True:
            receiver.write('RECV ') # Flag to recv
            if receiver.in_waiting:
                hex_string = receiver.read(8)
                # Looking for start of text
                if hex_string == '2020202':
                    print ("--- START OF TEXT ---")
                    state = 1
                elif state == 1:
                    try:
                        # Looking for end of text
                        if hex_string == '3030303':
                            receiver.write('#') # Flag to end listening
                            print ("\n--- END OF TEXT ---")
                            break
                        # Check and modify the length of string to 8 HEX char
                        if len(hex_string) < 8:
                            hex_string = hex_string.zfill(8)
                        # Convert to ASCII string
                        hex_list= map(''.join, zip(*[iter(hex_string)]*2))
                        ascii_string = "".join([chr(int("0x"+each_hex,0)) for each_hex in hex_list])
                        sys.stdout.write(ascii_string)
                        sys.stdout.flush()
                    except ValueError:
                        print("\n ERROR! UNABLE TO DECODE STRING!")
    except KeyboardInterrupt:
        print ("\nThank you for using the program!")
        sys.exit()  # Exits the program
