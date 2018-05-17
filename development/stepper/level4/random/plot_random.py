#!/usr/bin/env python2

'''
Python program to plot the numbers generated with the Entropy library
Author: Qcumber 2018
'''

import numpy as np
import matplotlib.pyplot as plt

numbers = np.genfromtxt("numbers.txt")

x = numbers // 2**16
y = numbers % 2**16

plt.scatter(x, y, s=1)
plt.xlim([0,2**16])
plt.xticks(np.arange(0, 2**16+1, step=2**14))
plt.ylim([0,2**16])
plt.yticks(np.arange(0, 2**16+1, step=2**14))

plt.title("'Random' numbers with Entropy library")
plt.savefig("random_fig.pdf")

plt.show()
