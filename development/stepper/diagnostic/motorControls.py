"""
Modified by: Xi Jie
Package for Motorstepper controls for QCamp 2018
"""
import serial
import time
class MotorControl(object):
# Module for communicating with the arduino analog pin
    baudrate = 9600 # Arduino baudrate

    def __init__(self, port):
        self.serial = serial.Serial(port, timeout=3)

        stuck_flag = True
        while(stuck_flag):
            self.serial.write('ANG? ')
            if not self.serial.in_waiting:
                # print("Stuck... Retrying")
                self.serial = serial.Serial(port, timeout=3)
                continue
            else:
                time.sleep(1)
               	self.serial.reset_input_buffer()
                print("Program Launched Successfully")
                stuck_flag = not stuck_flag

    def close_port(self):
        self.serial.close()

    def get_voltage(self):
        self.serial.write('VOLT? ')
        voltage = self.readline_fix() # Remove /n
        return voltage

    def set_angle(self,angle):
    	#Sets the absolute angle of the motor stepper
    	curr_offset = self.get_offset()
    	self.serial.write('SETANG '+str(angle) + ' ')
    	self.readline_fix()

    def get_angle(self):
    	#Gets the absolute angle of the motor stepper
    	self.serial.write('ANG? ')
    	angle = self.readline_fix()
    	return angle

    def set_offset(self,angle):
    	#Sets the offset angle of the motor stepper at H polarisation
    	self.serial.write('SETHOF '+str(angle) + ' ')
    	self.readline_fix()

    def get_offset(self):
    	#Gets the offset angle of the motor stepper at H polarisation
    	self.serial.write('HOF? ')
        angle = self.readline_fix()
    	return angle

    def power_on(self):
    	#Powers on laser
    	self.serial.write("LASON ")
    	self.readline_fix()

    def readline_fix(self):
        while(True):
            if self.serial.in_waiting:
                return self.serial.readline()[:-2]

    def power_off(self):
    	#Powers off laser
    	self.serial.write("LASOFF ")
    	self.readline_fix()