#!/usr/bin/env python2

'''
Python program to estimate the entropy and compression length from
the user input random numbers.
Author: Qcumber 2018
'''

print "Loading libraries..."

from bientropy import bien, tbien
import zlib

numstr = str(raw_input("Please enter the random numbers: \n"))
numlen = len(str(numstr))

print "You have entered", numlen, "numbers."

# Find the BiEn and tbien
bien_res = bien(numstr)
tbien_res = tbien(numstr)
print "\nBiEn:", bien_res
print "TBiEn:", tbien_res

# Find the compression
print "\nTrying the compression..."
comp_str = zlib.compress(numstr)
print comp_str
comp_len = len(comp_str)
print "\nThe compressed size is", comp_len
print "Compression ratio is", float(comp_len)/numlen
