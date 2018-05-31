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
import string

from PyQt4 import QtGui, uic
from PyQt4.QtCore import QTimer
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
from tabulate import tabulate
from collections import Counter

import pyqtgraph as pg
import Queue
import threading
import json
import numpy as np

form_class = uic.loadUiType("guiInterceptor.ui")[0]

def find_noise(x):
	"""guesses the noise floor as the most frequently occuring value"""
	noise = Counter(x).most_common(1)[0][0]
	# print noise
	return noise

def tohex(val, nbits):
	# Function to convert to hex, with a predefined nbits
	return hex((val + (1 << nbits)) % (1 << nbits))

def apply_mask_16(unkey_bin,matchbs_bin):
	"""
	Applies mask matchbs_hex to unkey_bin
	"""
	# Performing sifting process
	# matchbs_bin = np.binary_repr((int(matchbs_hex, 0)), width=16)
	siftmask_bin = ''
	for i in range(16): # 16 bits
	    if matchbs_bin[i] == '0' :
	        siftmask_bin += 'X'
	    elif matchbs_bin[i] == '1':
	        siftmask_bin += unkey_bin[i]
	#print "\nMatched key bits:",\
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
	#siftkey_bin = siftkey_bin.zfill(16) # pad to make length 16 bit
	return siftkey_bin

def apply_mask_n16(unkey_bin,matchbs_bin):
	"""
	Sifts n x 16 bit binary unkey_bin in groups of 16.
	"""
	# print len(matchbs_bin)
	siftkey_vec = []
	#print len(matchbs_bin)
	for n in np.arange(len(matchbs_bin)//16):
		masked = apply_mask_16(unkey_bin[n*16:(n+1)*16],matchbs_bin[n*16:(n+1)*16])
		#print(n, '\t', masked)
		siftkey_vec.append(masked)
	# print siftkey_vec
	siftkey_bin = ''.join(siftkey_vec)
	return siftkey_bin

def kclassify(data, numClasses=5):
	"""
	Classify 1-dimensional data into classes using KMeans algorithm
	5 classes are a default, refering to noise, and the four polarisations to be detected.

	Returns
	labels: list of classes to which each data point belongs to, len(data) long
	means: list of class means, len(np.unique(labels)) long
	"""
	# Classify
	km = KMeans(n_clusters=numClasses)
	km.fit(data.reshape(-1,1))
	km.predict(data.reshape(-1,1))
	labels = km.labels_

	# Class Means
	means = []
	# spreads = []
	for label in np.unique(labels):
	    means.append(np.mean(data[labels==label]))
	    # spreads.append(np.std(data[labels==label]))
	return np.array(labels), np.array(means)

def kclassify2D(x,y, numClasses=5):
	"""
	Classify 2-dimensional data into classes using KMeans algorithm
	5 classes are a default, refering to noise, and the four polarisations to be detected.
	"""


	x = np.array(x)
	y = np.array(y)
	data=np.array(zip(x,y)).reshape([-1,2])

	# Normalise
	x = normalize(x.reshape([-1,1]),axis=0)
	y = normalize(y.reshape([-1,1]),axis=0)

	dataNormed=np.array(zip(x,y)).reshape([-1,2])
	# print(x,y)
	# Classify
	km = KMeans(n_clusters=numClasses, algorithm="full")
	km.fit(dataNormed)
	km.predict(dataNormed)
	labels = km.labels_

	# Class & Means, Spreads
	means = []
	means2 = []
	spreads = []
	spreads2 = []
	classes = np.unique(labels)

	for label in classes:
	    means.append(np.mean(data[:,0][labels==label]))
	    means2.append(np.mean(data[:,1][labels==label]))
	    spreads.append(np.std(data[:,0][labels==label]))
	    spreads2.append(np.std(data[:,1][labels==label]))
	# print('kmeans labels = {}'.format(list(labels)))
	return np.array(list(labels)), np.array(classes), np.array(zip(means,means2)), np.array(zip(spreads,spreads2))

def hist(signals, numbins=200):
	"""
	Returns bin-centered histogram
	"""
	freq, bins = np.histogram(signals,numbins)
	step = bins[1]-bins[0]
	bins = bins[:-1]+step/2
	return freq, bins, step

def remove_adjacent_duplicates(a):
    undup = []
    # a = np.array(a)
    # print 'shape = {}'.format(a.shape)
    for i in np.arange(len(a)):
        if i==0: #no previous element to compare with, first element gets included automatically
            undup.append(a[i])
        else:
            if a[i] != a[i-1]:
                undup.append(a[i])
    return np.array(undup)

def manualClassify(voltage, voltageClasses):
    """
    returns the class in aClasses that matches most to an element in a
    voltageClasses = [0,v0,v1,v2,v3]
    """
    # relabels indices 1,2,3,4 to polarisation labels 0,1,2,3
    # polarisationLabels = [0,0,1,2,3]
    # argmin finds the element position in voltageClasses that best matches voltage
    return np.argmin((voltage-voltageClasses)**2)

def remove_header(signals,numConstant=3):
	"""
	Removes the header that has the signature of a high voltage being numConstant number of points
	"""
	ds = np.diff(signals)

	# Finds non-zero signal regions
	starts = np.where(ds>0)[0]
	stops = np.where(ds<0)[0]
	# signal_plot.plot(starts)
	# Finds header regions
	header_starts=starts[stops-starts>numConstant]+1
	header_stops=stops[stops-starts>numConstant]

	# Removes header regions
	headerless_signal = [signal for i, signal in enumerate(signals) if not np.any((i>=header_starts)&(i<=header_stops))]
	return headerless_signal

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

		# Declaring GUI window
		QtGui.QMainWindow.__init__(self, parent)
		self.setupUi(self)
		# self.initialiseParameters()

		# initial params
		self.noise = 0.02
		self.header_removed = False
		self.duplicates_removed = False
		self.noise_removed = False
		# Bind event handlers (button & range)
		"""
		---List of Buttons---

		"""
		self.buttonStart.clicked.connect(self.buttonStart_clicked)
		self.buttonDecode.clicked.connect(self.buttonDecode_clicked)
		self.lineMask.textChanged.connect(self.lineMask_textChanged)
		self.buttonApplyMask.clicked.connect(self.buttonApplyMask_clicked)

		# Gets a list of avaliable serial ports to connect to and adds to combo box
		self.files = glob.glob('key_logger/*.dat')
		self.fileBox.addItems(np.sort(self.files))

		# Set Display Options
		np.set_printoptions(precision=2)

		# Initialise plots
		self.signal_plot.plotItem.getAxis('left').setPen((0,0,0))
		self.signal_plot.plotItem.getAxis('bottom').setPen((0,0,0))
		labelStyle = {'font': 'Arial', 'font-size': '16px'}
		self.signal_plot.setLabel('left', 'Signals', 'V',**labelStyle)
		self.signal_plot.setLabel('bottom', 'Time', 'a.u.',**labelStyle)

		# self.signal_plot_2.plotItem.getAxis('left').setPen((0,0,0))
		# self.signal_plot_2.plotItem.getAxis('bottom').setPen((0,0,0))
		# labelStyle = {'font': 'Arial', 'font-size': '16px'}
		# self.signal_plot_2.setLabel('left', 'Signal2', 'V',**labelStyle)
		# self.signal_plot_2.setLabel('bottom', 'Time', 'a.u.',**labelStyle)

		# self.histo_plot.plotItem.getAxis('left').setPen((0,0,0))
		# self.histo_plot.plotItem.getAxis('bottom').setPen((0,0,0))
		self.histo_plot.setLabel('left', 'Signal2', 'V', **labelStyle)
		self.histo_plot.setLabel('bottom', 'Signal1', 'V',**labelStyle)
		# self.histo_plot.setTickSpacing(minor=0.1)




	###########
	# BUTTONS #
	###########
	def buttonStart_clicked(self):

		# Clear plots
		self.signal_plot.clear()
		self.histo_plot.clear()

		# Import file
		self.file = str(self.fileBox.currentText())
		self.signals = np.loadtxt(self.file)
		self.dev1, self.dev2 = self.signals[:,0], self.signals[:,1]
		self.signal_plot.plot(self.dev1,symbol='o',symbolPen='g',pen='g')
		self.signal_plot.plot(self.dev2,symbol='o',symbolPen='y',pen='y')
		# Remove points that don't tally
		def tally(x,y,noise=self.noise):
			"""
			ensures that when x is a signal, y is a signal too
			otherwise, set both x and y to the noise level
			"""
			x = np.array(x)
			y = np.array(y)
			noiseX = find_noise(x)
			noiseY = find_noise(y)

			noTally = np.logical_xor(x>noise,y>noise)
			self.signal_plot.plot((noTally))

			for i in np.where(noTally):
				x[i] = noiseX
				y[i] = noiseY

			return x, y

		self.dev1, self.dev2 = tally(self.dev1,self.dev2)

		# KMeans
		self.labels2D, self.classes, self.voltageClasses2D, self.voltageSpreads2D = kclassify2D(self.dev1,self.dev2,numClasses=5)

		# Signal Plot
		self.signal_plot.plot(self.dev1,symbol='o',symbolPen='r',pen='r')
		self.signal_plot.plot(self.dev2,symbol='o',symbolPen='b',pen='b')
		self.signal_plot.plot(self.labels2D)

		# 2D scatter Plot
		colors=['r', 'g', 'b', 'c', 'm', 'y', 'w']
		[self.histo_plot.plot(self.dev1[self.labels2D==Class],
			self.dev2[self.labels2D==Class],
			symbolBrush=pg.mkBrush(colors[Class]),
			pen=None,
			symbol='o') for Class in self.classes]

		# Set Display Options
		np.set_printoptions(precision=2)
		# print(tabulate(zip(self.classes, self.voltageClasses2D, self.voltageSpreads2D)))

		# Reformat integer classes to alphabets to reduce confusion
		self.alphabeticalClasses = [list(string.ascii_uppercase)[Class] for Class in self.classes]

		classificationTable = tabulate(
			zip(self.alphabeticalClasses,
				self.voltageClasses2D[:,0],
				self.voltageSpreads2D[:,0],
				self.voltageClasses2D[:,1],
				self.voltageSpreads2D[:,1]),
			headers=['cluster','signal1(V)','error1(V)','signal2(V)','error2(V)']
		)
		self.text_ClusterReport.setText(classificationTable)


	def buttonDecode_clicked(self):
		"""
		Decode signal according to user's guess of which voltage is being assigned to which polarisation.
		"""

		# def raw_from_manual():
		# 	"""
		# 	Use user-assigned voltage classes to classify signal heights & assign polarisation
		# 	Returns the assigned polarisation list as the list rawKey
		# 	"""
		# 	try:
		# 		# Get voltage assignment to polarisation
		# 		v0 = float(self.lineEdit_0.text())
		# 		v1 = float(self.lineEdit_1.text())
		# 		v2 = float(self.lineEdit_2.text())
		# 		v3 = float(self.lineEdit_3.text())
		# 	except:
		# 		print('cannot convert voltage input to float!')

		# 	manualVoltageClasses = [0,v0,v1,v2,v3]

		# 	# Classify each signal according to which class it is closest to
		# 	# Returns one of the integer labels [0, 1, 2, 3, 4] corresponding [0,..,v3]
		# 	manualLabels = [manualClassify(signal,manualVoltageClasses) for signal in self.signals]

		# 	# Removes headers
		# 	manualLabels = remove_header(manualLabels)
		# 	# self.signal_plot.plot(manualLabels,color='blue')

		# 	# Remove duplicate entries: only unique entries carry information
		# 	manualLabels = remove_adjacent_duplicates(manualLabels)

		# 	# Remove noise floor
		# 	manualLabels = manualLabels[manualLabels!=0]

		# 	# Henceforth rawKey refers to POLARISATION ENCODED KEY (unsifted through basis mask)
		# 	# Downshift labels so exclude noise label
		# 	rawKey = manualLabels-1
		# 	return rawKey

		def raw_from_ai():
			"""
			Uses cluster results and user's observations to assign polarisation.
			Returns the assigned polarisation list as the list rawKey
			"""
			try:
				# Get cluster assignment to polarisation
				c0 = str(self.lineEdit_0.text())
				c1 = str(self.lineEdit_1.text())
				c2 = str(self.lineEdit_2.text())
				c3 = str(self.lineEdit_3.text())
				c4 = str(self.lineEdit_4.text())
			except:
				print('cannot convert voltage input to float!')

			polAssignment = [c0,c1,c2,c3,c4] #[H,D,V,A,noise]
			polAssignment = [string.ascii_uppercase.index(c) for c in polAssignment] # convert to indices
			noiseLabel = polAssignment[-1]
			# Removes headers
			if self.header_removed==False:
				self.labels2D = remove_header(self.labels2D)
				self.header_removed = True

			# Removes duplicates
			if self.duplicates_removed==False:
				self.labels2D = remove_adjacent_duplicates(self.labels2D)
				self.duplicates_removed=True

			# Removes noise
			if self.noise_removed==False:
				self.labels2D = self.labels2D[self.labels2D!=noiseLabel]
				self.noise_removed=True

			#print('shape={}'.format(self.labels2D.shape))

			rawKey = [np.where(polAssignment==label) for label in self.labels2D]
			#print(rawKey)
			return np.array(rawKey).flatten()

		rawKey = raw_from_ai()
		rawKey_string = ''.join([str(e) for e in rawKey])

		#print(rawKey_string)
		# Convert rawKey into binary form, respecting basis choice
		self.rawKey_bin = (rawKey>=2).astype('int') #0-->0, 1-->0, 2-->1, 3-->1
		self.rawKey_bin_string = ''.join([str(e) for e in self.rawKey_bin])

		# Convert to hex: assumes length of raw
		rawKey_hex = tohex(int("0b"+self.rawKey_bin_string, 2), len(rawKey))

		# Print raw key
		self.raw_key.setText('{} ({}={:.1f} x 16 bits)'.format(rawKey_string,len(rawKey),len(rawKey)*1./16))
		self.raw_key_bin.setText('{}'.format(self.rawKey_bin_string))
		self.raw_key_hex.setText('{}'.format(rawKey_hex))

	def lineMask_textChanged(self,text):
		"""Counts number of bits entered"""
		# self.text_maskNumBits.setText('{}'.format(len(text)))
		pass


	def buttonApplyMask_clicked(self):
		# Convert mask from hex to binary
		matchbs_hex = "0x"+str(self.lineMask.text())
		#print(len(self.lineMask.text()))
		matchbs_bin = np.binary_repr((int(matchbs_hex, 0)), width=4*len(self.lineMask.text()))

		# Apply mask in groups of 16 bits
		self.maskedKey = apply_mask_n16(self.rawKey_bin_string,matchbs_bin)
		#print '{}'.format(self.maskedKey)

		# Convert mask from binary to hex and display
		self.masked_signal.setText('{}'.format(self.maskedKey))
		self.masked_signal_hex.setText('{}'.format(tohex(int(self.maskedKey[:32],2),len(matchbs_bin))))

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	myWindow = MyWindowClass(None)
	myWindow.show()
	sys.exit(app.exec_())
