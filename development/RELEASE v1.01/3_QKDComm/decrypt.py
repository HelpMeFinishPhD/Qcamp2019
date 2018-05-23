#!/usr/bin/env python2

'''
Python wrapper program to decrypt the message using the secure key
The key is expanded with Mersenne Twister PRNG.
Author: Qcumber 2018
'''

import numpy as np
import random

print "\nWelcome to decrypt! Please enter the encrypted text:"
encryptedMessage = raw_input()

print "\nNow, please enter the key (in 32 bit hex):"
key = raw_input()
if len(key) == 8 and len(encryptedMessage)%2 == 0:
    # Convert to int representation
    key_int = int("0x"+key, 0)
    # Using the key as the seed
    random.seed(key_int)
    # Get an array of expanded key. Each element corresponds to a byte
    expKey_arr = [int(random.getrandbits(8)) for i in range(len(encryptedMessage)/2)]
    # Construct each byte of encrypted message to an array
    encrypted_arr = map(''.join, zip(*[iter(encryptedMessage)]*2))
    xorMessage = [int(encrypted_arr[i],16)^expKey_arr[i] for i in range(len(encryptedMessage)/2)]
    # Convert back to ascii
    message = [chr(xorMessage[i]) for i in range(len(encryptedMessage)/2)]
    message = ''.join(message)
    print "\nThe decrypted message is:"
    print message
    print "\nCongratulations! Thank you for using the program!"
else :
    print "Either the key is not 4 bytes, or the message length is incorrect. Please try again"
