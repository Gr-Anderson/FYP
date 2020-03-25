import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import argrelextrema


def filter_signal():
    plt.figure(num=None, figsize=(10, 5), dpi=80, facecolor="w", edgecolor="k")

    b, a = signal.butter(4, 0.25, analog=False)

    data = pd.read_csv("test_ecg.csv")
    sig = data["voltage"]

    sig_ff = signal.filtfilt(b, a, sig)

    plt.plot(sig_ff, color="#000000", linewidth=1)
    plt.axis('off')

    plt.savefig("images/ecg_test.png", dpi=150, quality=100, bbox_inches='tight')
    r_peak_detection(sig_ff)
    # plt.tight_layout()
    # plt.show()


def r_peak_detection(sig_ff):
    threshold = 400
    start = 400
    end = -100
    amended_sig = sig_ff[start:end]
    no_of_rows = amended_sig.shape[0]
    line_numbers = []
    theVoltage = []

    for i in range(0, no_of_rows):
        if amended_sig[i] > threshold:
            theVoltage.append(amended_sig[i])
        else:
            theVoltage.append(0)
        line_numbers.append(i)          
        
    ecg_plot = np.concatenate((theVoltage, line_numbers))

    r_peaks = argrelextrema(ecg_plot, np.greater, order=5)

    plt.figure(num=None, figsize=(10, 5), dpi=80, facecolor="w", edgecolor="k")
    plt.plot(theVoltage, color="#000000", linewidth=1)

    plt.scatter(r_peaks[0],ecg_plot[r_peaks[0]],linewidth=0.3, s=500, c='r')
    plt.savefig("images/r_peaks.png", dpi=150, quality=100, bbox_inches='tight')


def segment_signal():
    r_peaks_list  = str(r_peaks)

    r_peaks_list = r_peaks_list.split() #split string into a list
    del r_peaks_list[0] # first element is a string and of no use
    r_peaks_list[-1] = (r_peaks_list[-1].replace(']),)', ',')) # last element has a string at end

    for i in range(0, len(r_peaks_list)):
        r_peaks_list[i] = (r_peaks_list[i].replace(',',''))
        r_peaks_list[i] = int(r_peaks_list[i])

    combined_creation = True
    # plt.figure(num=None, figsize=(20,10), dpi=150, facecolor="w", edgecolor="k")
    for i in range (0, 5):
        segment_start = r_peaks_list[i]
        segment_end = r_peaks_list[i+1]
        
        extracted_segment = amended_sig[segment_start:segment_end]
        if combined_creation:
            combined_seg = np.zeros(len(extracted_segment) + 100)
            combined_creation = False
        for j in range(0,len(extracted_segment)):
            combined_seg[j] =  combined_seg[j] + extracted_segment[j]
        
    for k in range (0, len(combined_seg)):
        if combined_seg[k] != 0:
            combined_seg[k] = (combined_seg[k] // 5)

    combined_seg = np.trim_zeros(combined_seg)

    plt.figure(num=None, figsize=(10, 5), dpi=80, facecolor="w", edgecolor="k")
    plt.axis('off')
    plt.plot(extracted_segment, color="#000000", linewidth=1)

filter_signal()
segment_signal()



