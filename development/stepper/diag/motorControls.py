"""
Modified by: Xi Jie
Package for Motorstepper controls for QCamp 2018
"""
import serial

class MotorControl(object):
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

    def set_angle(self,angle):
    	#Sets the absolute angle of the motor stepper
    	curr_offset = self.get_offset()
    	self.serial.write('SETANG '+str(angle) + ' ')
    	return 'OK \n'

    def get_angle(self):
    	#Gets the absolute angle of the motor stepper
    	self.serial.write('ANG? ')
    	angle = self.serial.readline()[:-2]
    	return angle

    def set_offset(self,angle):
    	#Sets the offset angle of the motor stepper at H polarisation
    	self.serial.write('SETHOF '+str(angle) + ' ')
    	return 'OK \n'

    def get_offset(self):
    	#Gets the offset angle of the motor stepper at H polarisation
    	self.serial.write('HOF? ')
    	angle = self.serial.readline()[:-2]
    	return angle

    def power_on(self):
    	#Powers on laser
    	self.serial.write("LASON ")
    	return "OK \n"


    def power_off(self):
    	#Powers off laser
    	self.serial.write("LASOFF ")
    	return "OK \n"