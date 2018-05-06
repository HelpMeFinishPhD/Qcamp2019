#!/usr/bin/env python2

'''
Python wrapper program to send a string through the IR channel with
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
rep_wait_time = 0.3  # Wait time between packets (in s).
timeout = 0.1        # Serial timeout (in s).

# Opens the sender side serial port
sender = serial.Serial(serial_addr, baudrate, timeout=timeout)

while True:
    try:
        msg_string = "\n" +\
                     "NEC-string Protocol Sender Qcumber v1.00 \n" +\
                     "To exit the program, use Ctrl+C \n" +\
                     "Write your message here: \n"
        tosend_string = raw_input(msg_string)
        # Iterate and send the string
        sender.write(b'\x02\x02\x02\x02') # Start of text
        time.sleep(rep_wait_time)
        str_ptr = 0
        max_str = len(tosend_string)
        while True:
            str_packet = tosend_string[str_ptr:str_ptr+4]
            sender.write(str_packet)
            sys.stdout.write("\r{0}    ".format("Sending: "+str_packet))
            sys.stdout.flush()
            str_ptr += 4
            time.sleep(rep_wait_time)
            if str_ptr >= max_str:
                sender.write(b'\x03\x03\x03\x03') # End of text
                time.sleep(rep_wait_time)
                sys.stdout.write("\r{0}\n".format("Sending done!"))
                sys.stdout.flush()
                break
    except NameError:   # Catches nonsense input
        print ("Input error. Please try again!")
        pass    # Loop back again
    except KeyboardInterrupt:
        print ("\nThank you for using the program!")
        sys.exit()  # Exits the program
