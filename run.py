# import time
# import serial
# import sqlite3
# import json
# import cv2
# import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt
# from scipy import signal
# from scipy.signal import argrelextrema
from BiometricSignal import *
from Segment import *
from Features import *
from Templates import *


# ----------------------------------------------------------------------------------------------
#                               CODE FOR TESTING BiometricSignal
# ----------------------------------------------------------------------------------------------

TEST_signal = BiometricSignal()
TEST_filtered_signal = TEST_signal.filter_captured_signal()
TEST_amended_signal = TEST_signal.amend_signal(TEST_filtered_signal)
TEST_r_peaks = TEST_signal.find_r_peaks(TEST_filtered_signal, TEST_amended_signal)

# print (TEST_signal.r_peaks)
# print(type(TEST_signal))

# ----------------------------------------------------------------------------------------------
#                               CODE FOR TESTING Segment
# ----------------------------------------------------------------------------------------------

TEST_segment = Segment(TEST_signal)
# print(type(TEST_segment.standardised_mean_segment))

# ----------------------------------------------------------------------------------------------
#                               CODE FOR TESTING Features
# ----------------------------------------------------------------------------------------------

TEST_features = Features(TEST_segment.mean_segment)
# print(TEST_features.features_lower)
# print(TEST_features.features_higher)

# ----------------------------------------------------------------------------------------------
#                               CODE FOR TESTING Features
# ----------------------------------------------------------------------------------------------

TEST_template = Templates()



