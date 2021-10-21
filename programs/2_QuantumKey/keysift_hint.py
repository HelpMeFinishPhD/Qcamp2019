#!/usr/bin/env python2

'''
Python wrapper program to simulate the key sifting process
in our BB84 QKD implementation (only for 16 bit keys).
Author: Qcumber 2018
'''

import sys
import time

# Get user to input hex
def inputhex():
    while True:
        unkey_hex = raw_input("").lower()#convert all to lower for convenience
        if(unkey_hex=='q'):
            print ("\nProgram exiting")
            exit()
        if(len(unkey_hex)==4 and all(c in '0123456789abcdef' for c in unkey_hex)):#checks if c is a 4 digit hex number
            break
        print ("Invalid input")
    return int(unkey_hex, 16)

while True:
    try:
        msg_string = "\n" +\
                     "Key sifting simulator for our BB84 QKD Scheme \n" +\
                     "To quit the program anytime, type q \n" +\
                     "1. Alice (sender)\n" +\
                     "2. Bob (receiver)\n" +\
                     "Your choice: "
        choice = raw_input(msg_string).lower()

        if choice == 'q':

            print ("\nProgram exiting")
            exit()

        elif choice == '1':

            print ("\nAlice, please input your value bits / unsifted key (in hex, max 4 hex):") 
            unkey_int = inputhex()
            unkey_bin = bin(unkey_int)[2:].zfill(16) # Binary string
            # Print the binary representation for each hex
            print "Binary representation:",\
                unkey_bin[:4], unkey_bin[4:8], unkey_bin[8:12], unkey_bin[12:16]

            print ("\nAlice, please input your basis choice (in hex, max 4 hex):")
            basisA_int = inputhex()
            basisA_bin = bin(basisA_int)[2:].zfill(16) # Binary string
            # Print the binary representation for each hex
            print "Binary representation:",\
                basisA_bin[:4], basisA_bin[4:8], basisA_bin[8:12], basisA_bin[12:16]

            print ("\nBob should have sent you something through public channel.")
            print ("\nAlice, please input Bob's basis choice (in hex, max 4 hex):")
            basisB_int = inputhex()
            basisB_bin = bin(basisB_int)[2:].zfill(16) # Binary string
            # Print the binary representation for each hex
            print "Binary representation:",\
                basisB_bin[:4], basisB_bin[4:8], basisB_bin[8:12], basisB_bin[12:16]

            matchbs_int = 0xffff ^ (basisA_int ^ basisB_int) # Negated XOR. Notice xoring with 1 flips it, we aren't using python ~ because it includes a sign bit for some reason
            matchbs_bin = bin(matchbs_int)[2:].zfill(16) # Binary string
            print ("\nThe matched basis is given below. Send this to Bob!")
            print "Hex representation:", hex(matchbs_int)[2:].zfill(4)
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
            siftkey_int = int(siftkey_bin, 2) # Get the int repr
            print "Hex representation:", hex(siftkey_int)[2:].zfill(4)

        elif choice == '2':

            print ("\nBob, please input your measurement result (in hex, max 4 hex):")
            unkey_int = inputhex()
            unkey_bin = bin(unkey_int)[2:].zfill(16) # Binary string
            # Print the binary representation for each hex
            print "Binary representation:",\
                unkey_bin[:4], unkey_bin[4:8], unkey_bin[8:12], unkey_bin[12:16]

            print ("\nBob, please input your basis choice (in hex, max 4 hex):")
            basisB_int = inputhex()
            basisB_bin = bin(basisB_int)[2:].zfill(16) # Binary string
            # Print the binary representation for each hex
            print "Binary representation:",\
                basisB_bin[:4], basisB_bin[4:8], basisB_bin[8:12], basisB_bin[12:16]

            print ("\nBob, send your basis choice to Alice through public channel!")
            print ("Wait for the response from Alice! It contains the matched basis.")

            print ("\nBob, please input the matched basis (in hex, max 4 hex):")
            matchbs_int = inputhex()
            matchbs_bin = bin(matchbs_int)[2:].zfill(16) # Binary string
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
            siftkey_int = int(siftkey_bin, 2) # Get the int repr
            print "Hex representation:", hex(siftkey_int)[2:].zfill(4)

        else:
            print ("Input error. Please try again!")
            pass    # Loop back again
    except NameError:   # Catches nonsense input
            print ("Input error. Please try again!")
            pass    # Loop back again
    except KeyboardInterrupt:
        print ("\nThank you for using the program!")
        sys.exit()  # Exits the program
