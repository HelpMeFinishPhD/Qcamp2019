#!/usr/bin/env python2

'''
Python wrapper program to encrypt a message using the secure key
The key is expanded with Mersenne Twister PRNG.
Author: Qcumber 2018
'''

import numpy as np
import random

print "\nWelcome to encrypt! Please enter the secure key (in 32 bit hex):"

key = raw_input()
if len(key) == 8:
    # Convert to int representation
    key_int = int("0x"+key, 0)
    # Using the key as the seed
    random.seed(key_int)
    # Ask user for the message
    print "\nPlease write down the message to encrypt below:"
    message = raw_input()
    # Get an array of expanded key. Each element corresponds to a byte
    expKey_arr = [int(random.getrandbits(8)) for i in range(len(message))]
    # Get the XORed message
    xorMessage = [ord(message[i])^expKey_arr[i] for i in range(len(message))]
    # Get the hex representation for the message
    xorMessage_hex = [hex(xorMessage[i])[2:].zfill(2) for i in range(len(message))]
    # Performing some cosmetics and obtain the encrypted Message
    encryptedMessage = ''.join(xorMessage_hex)
    print "\nThe encrypted message is:"
    print encryptedMessage
    print "\nTask completed. Thank you for using the program!"
else :
    print "The key is not 4 bytes. Please try again"
