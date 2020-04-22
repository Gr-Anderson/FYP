# import time
# import serial
# import sqlite3
# import json
# import cv2
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy import signal
# from scipy.signal import argrelextrema
from BiometricSignal import *
from Segment import *

from Templates import *


plt.style.use('seaborn')


# fig2, ax2 = plt.subplots()


# ----------------------------------------------------------------------------------------------
#                               CODE FOR TESTING BiometricSignal
# ----------------------------------------------------------------------------------------------

biosig = BiometricSignal()
biosig.filter_captured_signal()
biosig.amend_signal()
biosig.find_r_peaks()
biosig.standardise_signal()

fig1,ax1 = plt.subplots()
ax1.plot(biosig.standardised_signal, color='#444444')
ax1.set_title('Standardised ECG Signal')
ax1.set_ylabel('Millivolts')
ax1.set_xlabel('Time')

# ----------------------------------------------------------------------------------------------
#                               CODE FOR TESTING Segment
# ----------------------------------------------------------------------------------------------

seg = Segment(biosig)
fig2, ax2 = plt.subplots()
ax2.plot(seg.combined_seg, color='#444444')
ax2.set_title('Mean Segment')
ax2.set_ylabel('Millivolts')
ax2.set_xlabel('Time')

# ----------------------------------------------------------------------------------------------
#                               CODE FOR TESTING Templates
# ----------------------------------------------------------------------------------------------

templ = Templates('Sam')
a_user_template = templ.get_template('Sam')
fig3, ax3 = plt.subplots()
ax3.plot(seg.combined_seg, color='#444444')
ax3.set_title('An User\'s template')
ax3.set_ylabel('Millivolts')
ax3.set_xlabel('Time')
plt.tight_layout()
plt.show()




