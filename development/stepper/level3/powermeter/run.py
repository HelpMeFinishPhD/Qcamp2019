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
import pm_class as pm
import Queue
import threading
import json
import numpy as np

REFRESH_RATE = 0.1 # 100 ms
form_class = uic.loadUiType("gui.ui")[0]

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

        # Program is starting
        self.running = 1
        self.started = 0

        # Declaring GUI window
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.initialiseParameters()

        # Bind event handlers (button & range)
        self.buttonStart.clicked.connect(self.buttonStart_clicked)

        # Gets a list of avaliable serial ports to connect to and adds to combo box
        self.ports = glob.glob('/dev/ttyACM*')
        self.deviceBox.addItems(self.ports)

        # Initialise plots
        self.plotWidget.plotItem.getAxis('left').setPen((0,0,0))
        self.plotWidget.plotItem.getAxis('bottom').setPen((0,0,0))
        labelStyle = {'font': 'Arial', 'font-size': '16px'}
        self.plotWidget.setLabel('left', 'Power', 'V',**labelStyle)
        self.plotWidget.setLabel('bottom', '', '',**labelStyle)

        # Set timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.setInterval(REFRESH_RATE)
        self.timer.start()

        # Update status
        self.statusbar.showMessage("Ready to run ... Select your device!")

    def initialiseParameters(self):

        # Data for plotting
        self.xdata = np.arange(0,200,1)
        self.ydata = np.zeros(200)
        self.plot = self.plotWidget.plot(self.xdata, self.ydata, pen={'color':(255,0,0),'width':2})
        # Some cosmetics
        self.plotWidget.setLimits(xMin = self.xdata[0], xMax = self.xdata[-1])

    def update(self):

        # Updating the display value of optical powermeter
        if self.started == 1:
            try:
                self.voltage_A0 = float(self.powermeter.get_voltage())
                power_str = str(self.voltage_A0)
                self.labelPower.setText(power_str + " V")
                self.ydata = np.concatenate((self.ydata[1:],[self.voltage_A0]))
            except:
                # Sometime the serial channel needs to clear some junks
                pass
        else:
            self.labelPower.setText("OFF")

        # Plot data
        self.plot.setData(self.xdata, self.ydata)

    def buttonStart_clicked(self):

        if self.started == 0:

            # Start device
            self.powermeter = pm.AnalogPinComm(str(self.deviceBox.currentText()))
            # Initialising parameter and starting stuffs
            self.statusbar.showMessage("Measurement ongoing ...")
            self.buttonStart.setText("Stop")
            self.started = 1

        elif self.started == 1:

            self.started = 0
            self.statusbar.showMessage("Measurement stopped ...")
            # Change button appearance
            self.buttonStart.setText("Start")

    def cleanUp(self):
        print "Closing the program ... Good bye!"
        self.running = 0
        time.sleep(0.5)


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    myWindow = MyWindowClass(None)
    myWindow.show()
    app.aboutToQuit.connect(myWindow.cleanUp)
    sys.exit(app.exec_())
