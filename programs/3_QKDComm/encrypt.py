#!/usr/bin/env python2

'''
Python wrapper program to encrypt a message using the secure key
The key is expanded with Mersenne Twister PRNG.
Author: Qcumber 2018
'''

import random

print "\nWelcome to encrypt! Please enter the secure key (in 32 bit hex):"

key = raw_input()
if len(key) == 8:
    # Convert to int representation
    key_int = int(key, 16)
    # Using the key as the seed
    random.seed(key_int)
    # Ask user for the message
    print "\nPlease write down the message to encrypt below:"
    message = raw_input()
    # Get an array of expanded key. Each element corresponds to a byte
    expKey_arr = [int(random.getrandbits(8)) for i in range(len(message))]
    # Get the XORed message
    xorMessage = [ord(a) ^ b for a, b in zip(message, expKey_arr)]
    # Get the hex representation for the message
    encryptedMessage = ''.join(hex(i)[2:].zfill(2) for i in xorMessage)
    print "\nThe encrypted message is:"
    print encryptedMessage
    print "\nTask completed. Thank you for using the program!"
else :
    print "The key is not 4 bytes. Please try again"
