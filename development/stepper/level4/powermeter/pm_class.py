# -*- coding: utf-8 -*-
"""
Created on Mon Aug 25 19:12:31 2014

@author: nick
"""

import serial

class AnalogPinComm(object):
# Module for communicating with the arduino analog pin
    baudrate = 9600 # Arduino baudrate

    def __init__(self, port):
        self.serial = self._open_port(port)

    def _open_port(self, port):
        ser = serial.Serial(port, timeout=1)
        return ser

    def close_port(self):
        self.serial.close()

    def get_voltage(self):
        self.serial.write('VOLT? ')
        voltage = self.serial.readline()[:-2] # Remove /n
        return voltage

if __name__ == '__main__':
    import time
    powermeter = AnalogPinComm("/dev/ttyACM1")

    start = time.time()
    i=0
    while i <100:
        print (powermeter.get_voltage())
        i += 1
    end = time.time()

    print "Waktu", end - start
