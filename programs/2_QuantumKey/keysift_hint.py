#!/usr/bin/env python2

'''
Python wrapper program to simulate the key sifting process
in our BB84 QKD implementation (only for 16 bit keys).
Author: Qcumber 2018
'''

import sys
import time
import numpy as np

# Function to convert to hex, with a predefined nbits
def tohex(val, nbits):
  return hex((val + (1 << nbits)) % (1 << nbits))

while True:
    try:
        msg_string = "\n" +\
                     "Key sifting simulator for our BB84 QKD Scheme \n" +\
                     "To exit the program, use Ctrl+C \n" +\
                     "1. Alice (sender)\n" +\
                     "2. Bob (receiver)\n" +\
                     "Your choice: "
        choice = input(msg_string)
        if choice == 1:

            print ("\nAlice, please input your value bits / unsifted key (in hex, max 4 hex):")
            unkey_hex = raw_input("")
            unkey_int = int("0x"+unkey_hex[:4], 0)
            unkey_bin = np.binary_repr(unkey_int, width=16) # Binary string
            # Print the binary representation for each hex
            print "Binary representation:",\
                unkey_bin[:4], unkey_bin[4:8], unkey_bin[8:12], unkey_bin[12:16]

            print ("\nAlice, please input your basis choice (in hex, max 4 hex):")
            basisA_hex = raw_input("")
            basisA_int = int("0x"+basisA_hex[:4], 0)
            basisA_bin = np.binary_repr(basisA_int, width=16) # Binary string
            # Print the binary representation for each hex
            print "Binary representation:",\
                basisA_bin[:4], basisA_bin[4:8], basisA_bin[8:12], basisA_bin[12:16]

            print ("\nBob should have sent you something through public channel.")
            print ("\nAlice, please input Bob's basis choice (in hex, max 4 hex):")
            basisB_hex = raw_input("")
            basisB_int = int("0x"+basisB_hex[:4], 0)
            basisB_bin = np.binary_repr(basisB_int, width=16) # Binary string
            # Print the binary representation for each hex
            print "Binary representation:",\
                basisB_bin[:4], basisB_bin[4:8], basisB_bin[8:12], basisB_bin[12:16]

            matchbs_int = ~ (basisA_int ^ basisB_int) # Negative of exclusive OR.
            matchbs_hex = tohex(matchbs_int, 16) # 16 bits
            matchbs_int = int(matchbs_hex, 0) # Need convert again from hex
            # Note: This is to trim down the integer back to 16 bit.
            # The negation in the bitwise operation introduces a sign flip at the 17th bit.
            matchbs_bin = np.binary_repr(matchbs_int, width=16) # Binary string
            print ("\nThe matched basis is given below. Send this to Bob!")
            print "Hex representation:", matchbs_hex[2:].zfill(4)
            print "Binary representation:",\
                matchbs_bin[:4], matchbs_bin[4:8], matchbs_bin[8:12], matchbs_bin[12:16]

            # Performing sifting process
            siftmask_bin = ''
            for i in range(16): # 16 bits
                if matchbs_bin[i] == '0' :
                    siftmask_bin += 'X'
                elif matchbs_bin[i] == '1':
                    siftmask_bin += unkey_bin[i]
            print "\nMatched key bits:",\
                siftmask_bin[:4], siftmask_bin[4:8], siftmask_bin[8:12], siftmask_bin[12:16]
            # Remove all the X'es
            siftkey_bin = ''
            siftkey_len = 0
            for bit in siftmask_bin:
                if bit is 'X':
                    pass
                else:
                    siftkey_bin += bit
                    siftkey_len += 1
            siftkey_bin = siftkey_bin.zfill(16) # pad to make length 16 bit

            # Print final result
            print "\nCongrats! You obtain", siftkey_len, "bits key."
            print "Sifted key bits:",\
                siftkey_bin[:4], siftkey_bin[4:8], siftkey_bin[8:12], siftkey_bin[12:16]
            siftkey_int = int("0b"+siftkey_bin, 0) # Get the int repr
            siftkey_hex = tohex(siftkey_int, 16) # 16 bits
            print "Hex representation:", siftkey_hex[2:].zfill(4)


        elif choice == 2:

            print ("\nBob, please input your measurement result (in hex, max 4 hex):")
            unkey_hex = raw_input("")
            unkey_int = int("0x"+unkey_hex[:4], 0)
            unkey_bin = np.binary_repr(unkey_int, width=16) # Binary string
            # Print the binary representation for each hex
            print "Binary representation:",\
                unkey_bin[:4], unkey_bin[4:8], unkey_bin[8:12], unkey_bin[12:16]

            print ("\nBob, please input your basis choice (in hex, max 4 hex):")
            basisB_hex = raw_input("")
            basisB_int = int("0x"+basisB_hex[:4], 0)
            basisB_bin = np.binary_repr(basisB_int, width=16) # Binary string
            # Print the binary representation for each hex
            print "Binary representation:",\
                basisB_bin[:4], basisB_bin[4:8], basisB_bin[8:12], basisB_bin[12:16]

            print ("\nBob, send your basis choice to Alice through public channel!")
            print ("Wait for the response from Alice! It contains the matched basis.")

            print ("\nBob, please input the matched basis (in hex, max 4 hex):")
            matchbs_hex = raw_input("")
            matchbs_int = int("0x"+matchbs_hex[:4], 0)
            matchbs_bin = np.binary_repr(matchbs_int, width=16) # Binary string
            # Print the binary representation for each hex
            print "Binary representation:",\
                matchbs_bin[:4], matchbs_bin[4:8], matchbs_bin[8:12], matchbs_bin[12:16]

            # Performing sifting process
            siftmask_bin = ''
            for i in range(16): # 16 bits
                if matchbs_bin[i] == '0' :
                    siftmask_bin += 'X'
                elif matchbs_bin[i] == '1':
                    siftmask_bin += unkey_bin[i]
            print "\nMatched key bits:",\
                siftmask_bin[:4], siftmask_bin[4:8], siftmask_bin[8:12], siftmask_bin[12:16]
            # Remove all the X'es
            siftkey_bin = ''
            siftkey_len = 0
            for bit in siftmask_bin:
                if bit is 'X':
                    pass
                else:
                    siftkey_bin += bit
                    siftkey_len += 1
            siftkey_bin = siftkey_bin.zfill(16) # pad to make length 16 bit

            # Print final result
            print "\nCongrats! You obtain", siftkey_len, "bits key."
            print "Sifted key bits:",\
                siftkey_bin[:4], siftkey_bin[4:8], siftkey_bin[8:12], siftkey_bin[12:16]
            siftkey_int = int("0b"+siftkey_bin, 0) # Get the int repr
            siftkey_hex = tohex(siftkey_int, 16) # 16 bits
            print "Hex representation:", siftkey_hex[2:].zfill(4)

        else:
            print ("Input error. Please try again!")
            pass    # Loop back again
    except NameError:   # Catches nonsense input
            print ("Input error. Please try again!")
            pass    # Loop back again
    except KeyboardInterrupt:
        print ("\nThank you for using the program!")
        sys.exit()  # Exits the program
