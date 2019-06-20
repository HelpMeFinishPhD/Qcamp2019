#!/usr/bin/env python2

'''
Python wrapper program to decrypt the message using the secure key
The key is expanded with Mersenne Twister PRNG.
Author: Qcumber 2018
'''

import random

print "\nWelcome to decrypt! Please enter the encrypted text:"
encryptedMessage = raw_input()

print "\nNow, please enter the key (in 32 bit hex):"
key = raw_input()
if len(key) == 8:
    # Convert to int representation
    key_int = int(key, 16)
    # Using the key as the seed
    random.seed(key_int)
    # Get an array of expanded key. Each element corresponds to a byte
    expKey_arr = [int(random.getrandbits(8)) for i in range(len(encryptedMessage)/2)]
    # Convert encrypted message to a string
    encrypted_str = ('0'*(len(encryptedMessage) % 2)+encryptedMessage).decode('hex')
    xorMessage = [ord(a) ^ b for a, b in zip(encrypted_str, expKey_arr)]
    # Convert back to ascii
    message = ''.join(chr(i) for i in xorMessage)
    print "\nThe decrypted message is:"
    print message
    print "\nCongratulations! Thank you for using the program!"
else:
    print "Either the key is not 4 bytes, or the message length is incorrect. Please try again"
    print len(key)
    print len(encryptedMessage)

