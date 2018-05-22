#!/usr/bin/env python2

'''
Python wrapper program to send 32 bits QKD keys via
quantum and classial channel
Author: Qcumber 2018
'''

import serial
import sys
import time

# Parameter
rep_wait_time = 0.3  # Wait time between IR packets (in s).
wait_till_sync = 1   # Time to wait for Bob (until we are sure he is ready).

''' Helper functions '''

# Function to convert to hex, with a predefined nbits
def tohex(val, nbits):
    return hex((val + (1 << nbits)) % (1 << nbits))

def send4BytesC(message_str):
    if len(message_str) == 4:
        deviceC.write('SEND ') # Send identifier [BEL]x3 + A
        deviceC.write(b'\x07\x07\x07' + 'A') # This is Alice (sender)
        time.sleep(rep_wait_time)
        deviceC.write('SEND ') # Send message
        deviceC.write(message_str)
    else:
        print "The message is not 4 bytes. Please check again"

def recv4BytesC():
    deviceC.write('RECV ') # Flag to recv (the header)
    state = 0   # 0: waiting for STX, 1: transmitting/ wait for ETX
    while True: # Block until receives a reply
        if deviceC.in_waiting:
            hex_string = deviceC.read(8)
            if hex_string == '7070742':  # 07-[BEL], 42-B (Header from Bob)
                # print ("Received message!") # Debug
                deviceC.write('RECV ')   # Receive the message
                state = 1
            elif state == 1:
                break
    # Convert to ASCII string
    hex_list = map(''.join, zip(*[iter(hex_string)]*2))
    ascii_string = "".join([chr(int("0x"+each_hex,0)) for each_hex in hex_list])
    return ascii_string

def sendKeyQ():
    print "Generating random polarisation sequence..."
    # Randomising polarisation choice and run the sequence
    deviceQ.write('RNDSEQ ')
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
            reply_str = deviceQ.readlines()[0][:-1] # Remove the /n
            break
    # Obtain the binary string repr for val and bas bits
    val_str = ""
    bas_str = ""
    for bit in reply_str:
        val_str += str(int(bit) // 2)
        bas_str += str(int(bit) % 2)
    # Run the sequence
    print "Running the sequence..."
    deviceQ.write('TXSEQ ')
    # Block until receive reply
    while True:
        if deviceQ.in_waiting:
            print deviceQ.readlines()[0][:-1] # Should display OK
            break
    # Return the value and basis binary strings
    return val_str, bas_str

def keySiftAliceC(valA_str, basA_str):
    # Zeroth step: convert the bin string repr to 32 bit int
    valA_str = int("0b"+valA_str, 0)
    basA_str = int("0b"+basA_str, 0)
    # First step: Listens to Bob's basis
    basB_hex = recv4BytesC()   # in hex
    basB_str = int("0x"+basB_hex, 0)
    # Second step: Compare Alice and Bob's basis
    matchbs_int = ~ (basA_int ^ basB_int) # Perform matching operation
    # Third step: Send this matched basis back to Bob
    matchbs_hex = tohex(matchbs_int, 16) # Get the hex from int
    send4BytesC(matchbs_hex[2:].zfill(4)) # Sends this hex to Bob
    # Fourth step: Perform key sifting (in binary string)
    matchbs_str = np.binary_repr(matchbs_int, width=16)
    siftmask_str = ''
    for i in range(16): # 16 bits
        if matchbs_str[i] == '0' :
            siftmask_str += 'X'
        elif matchbs_str[i] == '1':
            siftmask_str += valA_str[i]
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

# Start of the UI
print "Hi Alice, are you ready? Let's make the key!"

try:
    # Testing the public channel
    print "\nTesting the public channel..."

    print "You send --Test--"
    send4BytesC("Test")

    print "Bob replies", recv4BytesC()

    print "\nPublic channel seems okay... Testing the quantum device"


    print "Sending the quantum keys..."

    print "\nAttempt 1"
    time.sleep(wait_till_sync) # Wait until Bob is ready to receive key
    val_str, bas_str = sendKeyQ()
    print keySiftAliceC(val_str, bas_str)

except KeyboardInterrupt:
    # End of program
    deviceC.write('#') # Flag to force end listening
    print ("\nProgram interrupted. Thank you for using the program!")
    sys.exit()  # Exits the program
