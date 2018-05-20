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
form_class = uic.loadUiType("guiRcv.ui")[0]

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

		self.offset = 0 
		# Whether or not we started the device 
		self.deviceRunning = False
		self.measuring = False

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
		measureButton : Mesasure
		resetButton : Reset
		startScan : Scan
		setOffset : Set Offset
		autoOffset : autoOffset
		goToPol : go to polarisation
		goToAngle : go to relative angle
		"""
		self.buttonStart.clicked.connect(self.buttonStart_clicked)
		self.resetButton.clicked.connect(self.reset_params)
		self.measureButton.clicked.connect(self.measure)
		self.goToPol.clicked.connect(self.set_polarisation)
		self.goToAngle.clicked.connect(self.set_angle)
		self.startScan.clicked.connect(self.start_scan)
		self.setOffset.clicked.connect(self.set_offset)
		self.autoOffset.clicked.connect(self.auto_offset)

		# Gets a list of avaliable serial ports to connect to and adds to combo box
		self.ports = glob.glob('/dev/ttyACM*') + glob.glob('/dev/ttyUSB*')
		self.deviceBox.addItems(self.ports)

		# Initialise plots
		self.plotWidget.plotItem.getAxis('left').setPen((0,0,0))
		self.plotWidget.plotItem.getAxis('bottom').setPen((0,0,0))
		labelStyle = {'font': 'Arial', 'font-size': '16px'}
		self.plotWidget.setLabel('left', 'Power', 'V',**labelStyle)
		self.plotWidget.setLabel('bottom', 'Absolute Angle', '',**labelStyle)

		
		# Set timer
		self.timer = QTimer()
		self.timer.timeout.connect(self.update_measure)
		self.timer.setInterval(REFRESH_RATE)
		self.timer.start()
		

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
			self.buttonStart.setText("Stop")
			self.offset = self.motor.get_offset

			#Initialising the motors
			self.curr_angle = int(self.motor.get_angle())
			self.offset  = int(self.motor.get_offset())
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
			self.labelPower.setText("OFF")

	def reset_params(self):
		#Resets the polarisation,angle and offset fields to zero
		self.statusbar.showMessage("Resetting Parameters... Please Wait")
		self.update_angle(0)
		self.update_offset(0)
		self.statusbar.showMessage("Resetting Parameters... Done")

	def start_scan(self):
		if self.deviceRunning:
			#Scan through the angles, plot graph and display plot
			self.xdata = np.arange(-180+self.offset,181+self.offset,1)
			read_count = 0
			self.statusbar.showMessage("Scanning... Please Wait")
			while(read_count != 361):
				try:
					self.voltage_A0 = float(self.motor.get_voltage())
					power_str = str(self.voltage_A0)
					#Update angle on GUI
					self.update_angle(self.xdata[read_count])
					#self.labelPower.setText(power_str + " V")
					self.ydata[read_count] = self.voltage_A0
					read_count += 1
				except:
					# Sometime the serial channel needs to clear some junks
					pass
			self.scanned = True
			# Plot data
			self.plotWidget.setLimits(xMin = self.xdata[0], xMax = self.xdata[-1])
			self.plot.setData(self.xdata, self.ydata)
			self.statusbar.showMessage("Scanning... Done")
		else:
			self.labelPower.setText("OFF")

	"""
	def set_angle(self):
		#Change the absolute angle in GUI and here
		#Get angle on GUI
		angle_value = self.angleInput.value()
		self.statusbar.showMessage("Setting Angle... Please Wait")
		self.curr_angle = angle_value
		self.motor.set_angle(angle_value)
		self.statusbar.showMessage("Setting Angle... Done")
	"""

	def update_angle(self,angle_value):
		#Change the absolute angle in GUI and here
		self.statusbar.showMessage("Updating Angle... Please Wait")
		self.curr_angle = angle_value
		#Update angle on GUI
		self.angleInput.setValue(angle_value)
		self.motor.set_angle(angle_value)
		self.statusbar.showMessage("Updating Angle... Done")

	def update_offset(self,offset_value):
		#Change the angle in GUI and here
		self.statusbar.showMessage("Updating Offset... Please Wait")

		self.offset = offset_value
		self.offsetInput.setValue(int(offset_value))
		self.motor.set_offset(offset_value)
		#self.angleInput.setValue(0)
		self.statusbar.showMessage("Updating Offset... Done")
		return None

	def set_offset(self):
		#Set offset angle at current angular position
		offset_value = self.offsetInput.value()
		self.update_offset(offset_value)
		return None

	def set_angle(self):
		#Set absolute angle 
		abs_angle = self.angleInput.value()
		self.update_angle(abs_angle)
		return None

	def set_polarisation(self):
		#Set the polarisation
		#The polarisation number
		pol_number = self.polInput.value()
		self.update_angle(pol_number*45+self.offset)
		return None

	def auto_offset(self):
		#TO BE COMPLETED
		#From latest plot, find offset and set offset to that value

		#fitted_angle = 
		#Use set_offset to do the last part
		self.set_offset(fitted_angle)
		return None

	def measure(self):
		if self.deviceRunning:
			if not self.measuring:
				self.measuring = not self.measuring
				self.measureButton.setText("Stop Measure")
			else:
				self.measureButton.setText("Start Measure")
		else:
			self.measuring = not self.measuring
			self.labelPower.setText("OFF")

	def update_measure(self):
		#If we are measuring
		if self.measuring:
			try:
				self.voltage_A0 = float(self.motor.get_voltage())
				power_str = str(self.voltage_A0)
				self.labelPower.setText(power_str + " V")
			except:
				# Sometime the serial channel needs to clear some junks
				pass
			#self.scanned = True
		else:
			self.labelPower.setText("OFF")

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
