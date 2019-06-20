ariana@Ariana ~/D/S/P/Y/Q/Q/p/3_QKDComm> cat send_32bitQKD.py 
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


def send4BytesC(message_str):
    if len(message_str) == 4:
        deviceC.write('SEND ')  # Send identifier [BEL]x3 + A
        deviceC.write(b'\x07\x07\x07' + 'A')  # This is Alice (sender)
        time.sleep(rep_wait_time)
        deviceC.write('SEND ')  # Send message
        deviceC.write(message_str)
        print message_str
    else:
        print "The message is not 4 bytes. Please check again"


def recv4BytesC():
    deviceC.reset_input_buffer()  # Flush all the garbages
    deviceC.write('RECV ')  # Flag to recv (the header)
    state = 0  # 0: waiting for STX, 1: transmitting/ wait for ETX
    while True:  # Block until receives a reply
        if deviceC.in_waiting:
            hex_string = deviceC.read(8)
            if hex_string == '7070742':  # 07-[BEL], 42-B (Header from Bob)
                # print ("Received message!")  # Debug
                deviceC.write('RECV ')  # Receive the message
                state = 1
            elif state == 1:
                break
    # Converting from hex to ASCII in 2.7
    ascii_string = ('0'*(len(hex_string) % 2) + hex_string).decode('hex')
    print ascii_string
    return ascii_string


def sendKeyQ():
    print "Generating random polarisation sequence..."
    # Randomising polarisation choice and run the sequence
    deviceQ.write('RNDSEQ ')
    # Block until receive reply
    while True:
        if deviceQ.in_waiting:
            print deviceQ.readlines()[0][:-1]  # Should display OK
            break
    # Find out what is the key
    deviceQ.write('SEQ? ')
    # Block until receive 1st reply
    while True:
        if deviceQ.in_waiting:
            reply_str = deviceQ.readlines()[0][:-1]  # Remove the /n
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
            print deviceQ.readlines()[0][:-1]  # Should display OK
            break
    # Return the value and basis binary strings
    print val_str, bas_str
    return val_str, bas_str


def keySiftAliceC(valA_str, basA_str):
    # Send ready confirmation to Alice
    send4BytesC("RDY!")
    print "Let's do it! Performing key sifting with Bob..."
    # Zeroth step: convert the bin string repr to 32 bit int
    valA_int = int(valA_str, 2)
    basA_int = int(basA_str, 2)
    # First step: Listens to Bob's basis
    basB_hex = recv4BytesC()   # in hex
    basB_int = int(basB_hex, 16)
    # Second step: Compare Alice and Bob's basis
    matchbs_int = 0xffff ^ (basA_int ^ basB_int)  # Perform matching operation, 0xffff^ is basically a not gate
    # Third step: Send this matched basis back to Bob
    send4BytesC(hex(matchbs_int)[2:].zfill(4))  # Sends this hex to Bob
    # Fourth step: Perform key sifting (in binary string)
    matchbs_str = bin(matchbs_int)[2:].zfill(16)
    siftmask_str = ''
    for i in range(16):  # 16 bits
        if matchbs_str[i] == '0':
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
    print siftmask_str, siftkey_str
    return siftkey_str

# Obtain device location
devloc_fileC = '../devloc_classical.txt'
devloc_fileQ = '../devloc_quantum.txt'
with open(devloc_fileC) as f:
    contentC = f.readlines()[0]
    if contentC[-1] == '\n':  # Remove an extra \n
        contentC = contentC[:-1]
with open(devloc_fileQ) as f:
    contentQ = f.readlines()[0]
    if contentQ[-1] == '\n':  # Remove an extra \n
        contentQ = contentQ[:-1]
serial_addrC = contentC
serial_addrQ = contentQ

# Other parameters declarations
baudrate = 9600      # Default in Arduino
rep_wait_time = 1    # 1 s wait time between each tries
timeout = 0.1        # Serial timeout (in s).

# Opens the sender side serial port
deviceC = serial.Serial(serial_addrC, baudrate, timeout=timeout)
deviceQ = serial.Serial(serial_addrQ, baudrate, timeout=timeout)

# Wait until the serial is ready
# Note: for some computer models, particularly MacOS, the program cannot
# talk to the serial directly after openin. Need to wait 1-2 second.
print "Opening the serial port..."
time.sleep(2)
print "Done\n"

# Secure key string (binary)
seckey_bin = ""
n_attempt = 1

# Start of the UI
print "Hi Alice, are you ready? Let's make the key!"

try:
    # Testing the public channel
    print "\nTesting the public channel..."

    print "You send --Test--"
    send4BytesC("Test")

    print "Bob replies", recv4BytesC()

    print "\nPublic channel seems okay... Sending the quantum keys..."

    # Performing key distribution
    while True:
        print "\nAttempt", n_attempt
        time.sleep(wait_till_sync)  # Wait until Bob is ready to receive key
        val_str, bas_str = sendKeyQ()
        time.sleep(wait_till_sync)  # Wait until Bob is ready to perform QKD
        key = keySiftAliceC(val_str, bas_str)
        seckey_bin = seckey_bin + key
        if len(seckey_bin) >= 32:  # If the key is longer than 32 bits, stop operation
            break
        else:
            print "Done! You've got", len(key), "bits. Total length:", len(seckey_bin), "bits."
            n_attempt += 1

    print "DONE. The task is completed."

    # You've got the key!
    seckey_bin = seckey_bin[:32]  # Trim to 32 bits
    seckey_hex = hex(int(seckey_bin, 2))[2:].zfill(8)
    # L would only appear if it would fit into a c signed long long int
    print "The 32 bit secret key is (in hex):", seckey_hex
    print "\n Congrats. Use the key wisely. Thank you!"

except KeyboardInterrupt:
    # End of program
    deviceC.write('#')  # Flag to force end listening
    print ("\nProgram interrupted. Thank you for using the program!")
    sys.exit()  # Exits the program
