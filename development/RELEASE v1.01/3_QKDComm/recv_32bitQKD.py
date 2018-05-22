#!/usr/bin/env python2

'''
Python wrapper program to send 32 bits QKD keys via
quantum and classial channel
Author: Qcumber 2018
'''

import serial
import sys
import time
import numpy as np

# IMPORTANT PARAMETER
threshold = 305  # Put the mean value from polarisation calibration (0 to 1023)

# Parameter
rep_wait_time = 0.3  # Wait time between packets (in s).

''' Helper functions '''

# Function to convert to hex, with a predefined nbits
def tohex(val, nbits):
    return hex((val + (1 << nbits)) % (1 << nbits))

def send4BytesC(message_str):
    if len(message_str) == 4:
        deviceC.write('SEND ') # Send identifier [BEL]x3 + B
        deviceC.write(b'\x07\x07\x07' + 'B') # This is Bob (receiver)
        time.sleep(rep_wait_time)
        deviceC.write('SEND ') # Flag to send
        deviceC.write(message_str)
    else:
        print "The message is not 4 bytes. Please check again"

def recv4BytesC():
    deviceC.write('RECV ') # Flag to recv (the header)
    state = 0   # 0: waiting for STX, 1: transmitting/ wait for ETX
    while True:            # Block until receives a reply
        if deviceC.in_waiting:
            hex_string = deviceC.read(8)
            if hex_string == '7070741':  # 07-[BEL], 41-A (Header from Alice)
                # print ("Received message!") # Debug
                deviceC.write('RECV ')   # Receive the message
                state = 1
            elif state == 1:
                break
    # Convert to ASCII string
    hex_list = map(''.join, zip(*[iter(hex_string)]*2))
    ascii_string = "".join([chr(int("0x"+each_hex,0)) for each_hex in hex_list])
    return ascii_string

def recvKeyQ():
    print "Generating random basis choices..."
    # Randomising the sequence
    deviceQ.write('RNDBAS ')
    # Block until receive reply
    while True:
        if deviceQ.in_waiting:
            print deviceQ.readlines()[0][:-1] # Should display OK
            break
    # Find out what is the key
    deviceQ.write('SEQ? ')
    # Block until receive 1st reply
    while True:
        if deviceQ.in_waiting:
            bas_str = deviceQ.readlines()[0][:-1] # Remove the /n
            break
    # Run the sequence
    print "Running the sequence and performing measurement..."
    deviceQ.write('RXSEQ ')
    # Block until receive reply
    while True:
        if deviceQ.in_waiting:
            mes_str = deviceQ.readlines()[0][:-1] # Remove the /n
            break
    print "Finished..."
    # Obtain the measured bits
    mes_arr = mes_str.split()
    res_str = ''
    for val in mes_arr:
        if int(val) > threshold: # Higher than threshold -> 0
            res_str += '0'
        else:               # Lower than threshold -> 1
            res_str += '1'
    return res_str, bas_str

def keySiftBobC(resB_str, basB_str):
    # Get ready confirmation from Alice
    recv4BytesC()
    print "Alice is ready! Performing key sifting with Alice..."
    # Zeroth step: convert the bin string repr to 32 bit int
    resB_int = int("0b"+resB_str, 0)
    basB_int = int("0b"+basB_str, 0)
    # First step: send the basis choice to Alice
    basB_hex = tohex(basB_int, 16) # Get the hex from int
    send4BytesC(basB_hex[2:].zfill(4)) # Sends this hex to Bob
    # Second step: Wait for her reply...
    matchbs_hex = recv4BytesC()   # in hex
    matchbs_int = int("0x"+matchbs_hex, 0)
    # Fourth step: Perform key sifting (in binary string)
    matchbs_str = np.binary_repr(matchbs_int, width=16)
    siftmask_str = ''
    for i in range(16): # 16 bits
        if matchbs_str[i] == '0' :
            siftmask_str += 'X'
        elif matchbs_str[i] == '1':
            siftmask_str += resB_str[i]
    # Remove all the X'es
    siftkey_str = ''
    for bit in siftmask_str:
        if bit is 'X':
            pass
        else:
            siftkey_str += bit
    # Return the final sifted key
    return siftkey_str

# Obtain device location
devloc_fileC = 'devloc_classical.txt'
devloc_fileQ = 'devloc_quantum.txt'
with open(devloc_fileC) as f:
    contentC = f.readlines()
serial_addrC = contentC[0][:-1]
with open(devloc_fileQ) as f:
    contentQ = f.readlines()
serial_addrQ = contentQ[0][:-1]

# Other parameters declarations
baudrate = 9600      # Default in Arduino
rep_wait_time = 1    # 1 s wait time between each tries
timeout = 0.1        # Serial timeout (in s).

# Opens the sender side serial port
deviceC = serial.Serial(serial_addrC, baudrate, timeout=timeout)
deviceQ = serial.Serial(serial_addrQ, baudrate, timeout=timeout)

# Secure key string (binary)
seckey_bin = ""
n_attempt = 1

# Start of the UI
print "Hi Bob, are you ready? Let's make the key!"

try:
    # Testing the public channel
    print "\nTesting the public channel..."

    print "Alice sends", recv4BytesC()

    print "You reply --OK!!--"
    send4BytesC("OK!!")

    print "\nPublic channel seems okay... Sending the quantum keys..."

    while True:
        print "\nAttempt", n_attempt
        res_str, bas_str = recvKeyQ()
        key = keySiftBobC(res_str, bas_str)
        seckey_bin = seckey_bin + key
        if len(seckey_bin) >= 32: # If the key is longer than 32 bits, stop operation
            break
        else:
            print "Done! You've got", len(key), "bits. Total length:", len(seckey_bin), "bits."
            n_attempt +=1

    print "DONE. The task is completed."

    # You've got the key!
    seckey_bin = seckey_bin[:32] # Trim to 32 bits
    seckey_hex = tohex(int("0b"+seckey_bin, 0), 16)
    print "The 32 bit secret key is (in hex):", seckey_hex[2:].zfill(4)
    print "\n Congrats. Use the key wisely. Thank you!"

except KeyboardInterrupt:
    # End of program
    deviceC.write('#') # Flag to force end listening
    print ("\nProgram interrupted. Thank you for using the program!")
    sys.exit()  # Exits the program
