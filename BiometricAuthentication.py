import time
import serial
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import argrelextrema

class BiometricSignal: 
    
    captured_signal_csv = "./assets/subject_raw_ecg.csv"

    def __init__(self):
        self.bio_signal = "test"

    def capture_signal(self):
        serial_data = serial.Serial("/dev/ttyACM1", 9600)
        serial_list = []
        capture_time = 5
        t_end = time.time() + capture_time

        time.sleep(2)

        while time.time() < t_end:
            while serial_data.inWaiting() == 0:
                pass
            temp_string = serial_data.readline()
            serial_string = (
                str(temp_string)
                .replace("b", "")
                .replace("'", "")
                .replace("\\r", "")
                .replace("\\n", "")
            )
            if len(serial_string) == 3:
                serial_list.append(int(serial_string))
        return serial_list


    def output_signal_to_csv(self, serial_list):
        with open(BiometricSignal.captured_signal_csv, "w") as ecg_file:
            ecg_file.write("voltage,\n")
            for item in serial_list:
                ecg_file.write("%s,\n" % item)
            ecg_file.write("0,")


    def filter_captured_signal(self):
        numerator, denominator = signal.butter(4, 0.25, analog=False)
        data = pd.read_csv(BiometricSignal.captured_signal_csv)
        sig = data["voltage"]
        filtered_signal = signal.filtfilt(numerator, denominator, sig)
        return filtered_signal
    
    
    def find_r_peaks(self):
        
        threshold = 400
        start = 400
        end = -100
        
        amended_signal = filtered_signal[start:end]
        no_of_rows = amended_signal.shape[0]
        line_numbers = []
        theVoltage = []


        for i in range(0, no_of_rows):
            if amended_signal[i] > threshold:
                theVoltage.append(amended_signal[i])
            else:
                theVoltage.append(0)
            line_numbers.append(i)    


        ecg_plot = np.concatenate((theVoltage, line_numbers))

        r_peaks = argrelextrema(ecg_plot, np.greater, order=5)
        
        return r_peaks
