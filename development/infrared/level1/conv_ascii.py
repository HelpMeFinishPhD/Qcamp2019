#!/usr/bin/env python2

# This program asks the user and converts between ASCII and binary/hex.
# Author: Qcumber 2018

import time
import sys

# Adding the STX and ETX features onto the chr function
def to_chr(int_input):
    if int_input == 2:
        return "--- START OF TEXT ---\n"
    elif int_input == 3:
        return "\n--- END OF TEXT ---"
    else:
        return chr(int_input)

while True:
    try:
        msg_string = "\n" +\
                     "ASCII converter Qcumber v1.00 \n" +\
                     "To exit the program, use Ctrl+C \n" +\
                     "1. ASCII string to hex and binary converter\n" +\
                     "2. Hex to ASCII string converter\n" +\
                     "3. Binary to ASCII string converter\n" +\
                     "Your choice: "
        choice = input(msg_string)
        if choice == 1:
            print ("Please input your ASCII string:")
            ascii_string = raw_input("")
            # Get the integer representation of each character
            int_list = [ord(char) for char in ascii_string]
            # Convert to hex and binary representation
            hex_string = " ".join([hex(each_int)[2:] for each_int in int_list])
            bin_string = " ".join([bin(each_int)[2:].zfill(8) for each_int in int_list])
            print ("Hexadecimal representation: " + hex_string)
            print ("Binary representation: \n" + bin_string)
        elif choice == 2:
            print ("Please input your hex string (separate each character with a space):")
            hex_string = raw_input("")
            # Get the integer representation of each character
            try:
                int_list = [int("0x"+hex_char,0) for hex_char in hex_string.split()]
                # Convert to ASCII string
                ascii_string = "".join([to_chr(each_int) for each_int in int_list])
                print ("ASCII string: \n" + ascii_string)
            except ValueError:
                print("Hex string can not be decoded. Please check your input!")
        elif choice == 3:
            print ("Please input your binary string (separate each character with a space):")
            bin_string = raw_input("")
            # Get the integer representation of each character
            try:
                int_list = [int("0b"+bin_char,0) for bin_char in bin_string.split()]
                # Convert to ASCII string
                ascii_string = "".join([to_chr(each_int) for each_int in int_list])
                print ("ASCII string: \n" + ascii_string)
            except ValueError:
                print("Binary string can not be decoded. Please check your input!")
        else:
            print ("Input error. Please try again!")
            pass    # Loop back again
    except NameError:   # Catches nonsense input
            print ("Input error. Please try again!")
            pass    # Loop back again
    except KeyboardInterrupt:
        print ("\nThank you for using the program!")
        sys.exit()  # Exits the program
