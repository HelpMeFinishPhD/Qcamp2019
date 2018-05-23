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
devloc_file = 'devloc_classical.txt'
with open(devloc_file) as f:
    content = f.readlines()
serial_addr = content[0][:-1]

# Other parameters declarations
baudrate = 9600      # Default in Arduino
rep_wait_time = 0.3  # Wait time between packets (in s).
timeout = 0.1        # Serial timeout (in s).

# Opens the device side serial port
device = serial.Serial(serial_addr, baudrate, timeout=timeout)

print "Qcumber ChatBox v1.00"
print "To exit the program, use Ctrl+C"

# Always listening, except when it is not...
while True:
    try:
        msg_string = "\n" +\
                     "You are now in sending mode. To change to listening mode, press ENTER.\n" +\
                     "Write the message you want to send below: \n"
        tosend_string = raw_input(msg_string)
        if tosend_string == "": # Nothing to send through
            pass
        else:   # Send the message lor
            # Iterate and send the string
            device.write('SEND ') # Flag to send
            device.write(b'\x02\x02\x02\x02') # Start of text
            time.sleep(rep_wait_time)
            str_ptr = 0
            max_str = len(tosend_string)
            while True:
                str_packet = tosend_string[str_ptr:str_ptr+4]
                device.write('SEND ') # Flag to send
                device.write(str_packet)
                sys.stdout.write("\r{0}    ".format("Sending: "+str_packet))
                sys.stdout.flush()
                str_ptr += 4
                time.sleep(rep_wait_time)
                if str_ptr >= max_str:
                    device.write('SEND ') # Flag to send
                    device.write(b'\x03\x03\x03\x03') # End of text
                    time.sleep(rep_wait_time)
                    sys.stdout.write("\r{0}\n".format("Sending done!"))
                    sys.stdout.flush()
                    break
        msg_string = "\n" +\
                     "You are now in listening mode.\n" +\
                     "Waiting to receive the message... \n"
        print (msg_string)
        state = 0 # 0 : waiting for STX, 1 : transmitting/ wait for ETX
        device.write('RECV ') # Flag to recv
        while True:
            if device.in_waiting:
                hex_string = device.read(8)
                device.write('RECV ') # Flag to recv
                # Looking for start of text
                if hex_string == '2020202':
                    print ("--- START OF TEXT ---")
                    state = 1
                elif state == 1:
                    try:
                        # Looking for end of text
                        if hex_string == '3030303':
                            device.write('#') # Flag to end listening
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
        device.write('#') # Flag to force end listening
        print ("\nThank you for using the program!")
        sys.exit()  # Exits the program
