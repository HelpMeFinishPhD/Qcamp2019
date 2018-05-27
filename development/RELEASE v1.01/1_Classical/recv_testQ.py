#!/usr/bin/env python2

'''
Python wrapper program to receive a string through the IR channel with
the NEC-string protocol.
Author: Qcumber 2018
'''

import serial
import sys
import time

# Text to send and verify
text = "Qc!8" # Maximum of 4 bytes / 4 characters

# Obtain device location
devloc_file = '../devloc_classical.txt'
with open(devloc_file) as f:
    content = f.readlines()[0]
    if content[-1] == '\n':  # Remove an extra \n
        content = content[:-1]
serial_addr = content

# Other parameters declarations
baudrate = 9600      # Default in Arduino
timeout = 0.1        # Serial timeout (in s).

# Opens the sender side serial port
receiver = serial.Serial(serial_addr, baudrate, timeout=timeout)

while True:
    try:
        print "Waiting for any incoming messages..."
        print "To exit the program, use Ctrl+C\n"
        receiver.reset_input_buffer() # Flush all the garbages
        receiver.write('RECV ') # Flag to recv
        while True:
            if receiver.in_waiting:
                hex_string = receiver.read(8)
                # Translating the text:
                try:
                    # Check and modify the length of string to 8 HEX char
                    if len(hex_string) < 8:
                        hex_string = hex_string.zfill(8)
                    # Convert to ASCII string
                    hex_list= map(''.join, zip(*[iter(hex_string)]*2))
                    ascii_string = "".join([chr(int("0x"+each_hex,0)) for each_hex in hex_list])
                    if ascii_string == text:
                        print "Received the text: ", ascii_string, ". Mission Successful"
                        print "To exit the program, use Ctrl+C\n"
                    else:
                        print "Receiving something that does not seem correct:", ascii_string
                        print "To exit the program, use Ctrl+C\n"
                    # Trying to receive again
                    receiver.reset_input_buffer() # Flush all the garbages
                    receiver.write('RECV ') # Flag to recv
                except ValueError:
                    print("\n ERROR! UNABLE TO DECODE STRING!")
    except KeyboardInterrupt:
        receiver.write('#') # Flag to force end listening
        print ("\nThank you for using the program!")
        sys.exit()  # Exits the program
