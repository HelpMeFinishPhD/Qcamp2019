#!/usr/bin/env python
"""
Created on May 2018

Modified from the QITlab program
@author: Adrian Utama

Powermeter for Arduino Analogread (PyQt) Version 1.01
"""

import sys
import glob
import time

from PyQt4 import QtGui, uic
from PyQt4.QtCore import QTimer
import pyqtgraph as pg
import motorControls as mc
import Queue
import threading
import json
import numpy as np

REFRESH_RATE = 0.1 # 100 ms
form_class = uic.loadUiType("guiSnd.ui")[0]

def insanity_check(number, min_value, max_value):
    ''' To check whether the value is out of given range'''
    if number > max_value:
        return max_value
    if number < min_value:
        return min_value
    else:
        return number

class MyWindowClass(QtGui.QMainWindow, form_class):

    def __init__(self, parent=None):

        # Whether or not we started the device 
        self.deviceRunning = False

        # Whether or not we have scanned
        self.scanned = False

        # Declaring GUI window
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.initialiseParameters()

	    # Bind event handlers (button & range)
        """
        ---List of Buttons---
        buttonStart : ON/OFF
        resetButton : Reset
        setOffset : Set Offset
        goToPol : go to polarisation
        goToAngle : go to relative angle
        """
        self.buttonStart.clicked.connect(self.buttonStart_clicked)
        self.resetButton.clicked.connect(self.reset_params)
        self.goToPol.clicked.connect(self.set_polarisation)
        self.goToAngle.clicked.connect(self.set_angle)
        self.setOffset.clicked.connect(self.set_offset)
        self.toggle.clicked.connect(self.toggle_laser)

        # Gets a list of avaliable serial ports to connect to and adds to combo box
        self.ports = glob.glob('/dev/ttyACM*') + glob.glob('/dev/ttyUSB*')
        self.deviceBox.addItems(self.ports)

        # Initialise plots
        self.plotWidget.plotItem.getAxis('left').setPen((0,0,0))
        self.plotWidget.plotItem.getAxis('bottom').setPen((0,0,0))
        labelStyle = {'font': 'Arial', 'font-size': '16px'}
        self.plotWidget.setLabel('left', 'Power', 'V',**labelStyle)
        self.plotWidget.setLabel('bottom', 'Absolute Angle', '',**labelStyle)

        """
        # Set timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.setInterval(REFRESH_RATE)
        self.timer.start()
		"""

        # Update status
        self.statusbar.showMessage("Ready to run ... Select your device!")

    def initialiseParameters(self):

        # Data for plotting
        self.xdata = np.arange(-180+self.offset,181+self.offset,1)
        self.ydata = np.zeros(361)
        self.plot = self.plotWidget.plot(self.xdata, self.ydata, pen={'color':(255,0,0),'width':2})
        # Some cosmetics
        self.plotWidget.setLimits(xMin = self.xdata[0], xMax = self.xdata[-1])


    ###########
    # BUTTONS #
	###########
	def buttonStart_clicked(self):

		#Turning on device for the first time
		if not self.deviceRunning:

            # Start device
            self.motor = mc.MotorControl(str(self.deviceBox.currentText()))
            # Initialising parameter and starting stuffs
            self.statusbar.showMessage("Device Running")
            self.laserOn = False
            self.labelPower.setText("OFF")
            self.buttonStart.setText("Stop")

            #Initialising the motors
            self.curr_angle = self.motor.get_angle()
            self.offset  = self.motor.get_offset()
            self.update_offset(self.offset)
            self.update_angle(self.curr_angle)
            self.deviceRunning = not self.deviceRunning


        else:

        	#Stop the device
            self.deviceRunning = not self.deviceRunning
            self.statusbar.showMessage("Device Stopped")
            # Change button appearance
            self.motor.close_port()
            self.buttonStart.setText("Start")
            self.laserOn = False
            self.labelPower.setText("OFF")
    def toggle_laser(self):
    	if self.laser:
    		#now laser is on, turn off laser
    		self.motor.power_off()
    		self.labelPower.setText("OFF")
    		self.laserOn = not self.laserOn

    	else:
    		#now laser if off, turn on laser
    		self.motor.power_on()
    		self.labelPower.setText("ON")
    		self.laserOn = not self.laserOn

	def reset_params(self):
		#Resets the polarisation,angle and offset fields to zero
		self.statusbar.showMessage("Resetting Parameters... Please Wait")
		self.update_angle(0)
		self.update_offset(0)
		self.statusbar.showMessage("Resetting Parameters... Done")

	def update_angle(self,angle_value):
		#Change the absolute angle in GUI and here
		self.statusbar.showMessage("Updating Angle... Please Wait")
		self.curr_angle = angle_value
		self.angleInput.setValue(angle_value)
		self.motor.set_angle(angle_value)
		self.statusbar.showMessage("Updating Angle... Done")

		return None

	def update_offset(self,offset_value):
		#Change the angle in GUI and here
		self.statusbar.showMessage("Updating Offset... Please Wait")

		self.offset = offset_value
		self.offsetInput.setValue(offset_value)
		self.motor.set_angle(offset_value)
		self.statusbar.showMessage("Updating Offset... Done")
		return None

	def set_offset(self):
		#Set offset angle at current angular position
		offset_value = self.offsetInput.value()
		self.update_offset(offset_value)
		return None

	def set_offset(self):
		#Set absolute angle 
		abs_angle = self.offsetInput.value()
		self.update_angle(abs_angle)
		return None
	
	def set_polarisation(self):
		#Set the polarisation
		#The polarisation number
		pol_number = self.polInput.value()
		self.update_angle(pol_number*45+self.offset)
		return None

    def cleanUp(self):
        print "Closing the program ... Good bye!"
        self.deviceRunning = False
        time.sleep(0.5)

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    myWindow = MyWindowClass(None)
    myWindow.show()
    app.aboutToQuit.connect(myWindow.cleanUp)
    sys.exit(app.exec_())
