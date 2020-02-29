import numpy as np
import cv2 as cv


def find_peaks(peas_list, y, x):
    for y_cors in range (y,3):
        for x_cors in range (x, image_x):
            if test_list[y_cors][x_cors] == 0:
                x = x_cors + 2
                if {y_cors, x_cors} not in peaks_list:
                    peaks_list.append({y_cors, x_cors})
                print(peaks_list)
                print("INNER")
                return x
        print("OUTER")
    return x
    
    
test_list = [ [1,1,1,1,1,1,1,1,1,1,1,1],
              [1,1,0,1,1,1,1,1,0,1,1,0],
              [1,1,1,1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1,1,1,1,1,1],]

image_x = 12
image_y = 3
x = 0
y = 0
peaks_list = []
keep_looping = True

while keep_looping:
#     print("X: ", x)
    if x < image_x:
        print("X: ", x)
        x = (find_peaks(peaks_list, y, x))
    else:
        keep_looping = False
        
        
print("X: ", x)
print("Y: ", y)

















# 
# # from IPython.display import display
# import matplotlib.pyplot as plt
# import numpy as np
# # import os
# # import shutil
# import wfdb
# from wfdb import processing


# def peaks_hr(sig, peak_inds, fs, title, figsize=(20, 10), saveto=None):
#     "Plot a signal with its peaks and heart rate"
#     hrs = processing.compute_hr(sig_len=sig.shape[0], qrs_inds=peak_inds, fs=fs)
    
#     N = sig.shape[0]
    
#     fig, ax_left = plt.subplots(figsize=figsize)
#     ax_right = ax_left.twinx()
    
#     ax_left.plot(sig, color='#3979f0', label='Signal')
#     ax_left.plot(peak_inds, sig[peak_inds], 'rx', marker='x', color='#8b0000', label='Peak', markersize=12)
#     ax_right.plot(np.arange(N), hrs, label='Heart rate', color='m', linewidth=2)

#     ax_left.set_title(title)

#     ax_left.set_xlabel('Time (ms)')
#     ax_left.set_ylabel('ECG (mV)', color='#3979f0')
#     ax_right.set_ylabel('Heart rate (bpm)', color='m')
#     ax_left.tick_params('y', colors='#3979f0')
#     ax_right.tick_params('y', colors='m')
#     if saveto is not None:
#         plt.savefig(saveto, dpi=600)
#     plt.show()


# record = wfdb.rdrecord('sampledata/100', sampfrom=0, sampto=2000, channels=[0])

# qrs_inds = processing.gqrs_detect(sig=record.p_signal[:,0], fs=record.fs)

# peaks_hr(sig=record.p_signal, peak_inds=qrs_inds, fs=record.fs,
#         title="GQRS peak detection on record 100")
    
# min_bpm = 20
# max_bpm = 230

# search_radius = int(record.fs * 60 / max_bpm)
# corrected_peak_inds = processing.correct_peaks(record.p_signal[:,0], peak_inds=qrs_inds,
#                                                search_radius=search_radius, smooth_window_size=150)


# print('Corrected gqrs detected peak indices:', sorted(corrected_peak_inds))
# peaks_hr(sig=record.p_signal, peak_inds=sorted(corrected_peak_inds), fs=record.fs,
#          title="Corrected GQRS peak detection on sampledata/100")
    

# from __future__ import division, print_function
# import pandas as pd
# import numpy as np
# from numpy.random import randn
# from numpy.fft import rfft
# from scipy import signal
# import matplotlib.pyplot as plt
# from matplotlib.pyplot import figure

# figure(num=None, figsize=(20, 10), dpi=80, facecolor="w", edgecolor="k")

# b, a = signal.butter(4, 0.25, analog=False)

# # Show that frequency response is the same
# impulse = np.zeros(1000)
# impulse[500] = 1

# # Applies filter forward and backward in time
# imp_ff = signal.filtfilt(b, a, impulse)

# # sig = np.cumsum(randn(800))  # Brownian noise
# data = pd.read_csv("test12.csv")
# sig = data["voltage"]

# sig_ff = signal.filtfilt(b, a, sig)

# # plt.plot(sig, color="red", label="Original", linewidth=3)
# # plt.plot(voltage, color="silver", label="Original")

# plt.plot(sig_ff, color="#3465a4", label="filtfilt", linewidth=5)
# plt.grid(True, which="both")


# plt.savefig("test02.png")
# plt.tight_layout()
# plt.show()

# from __future__ import division, print_function
# import numpy as np
# from numpy.random import randn
# from numpy.fft import rfft
# from scipy import signal
# import matplotlib.pyplot as plt

# b, a = signal.butter(4, 0.03, analog=False)

# # Show that frequency response is the same
# impulse = np.zeros(1000)
# impulse[500] = 1

# # Applies filter forward and backward in time
# imp_ff = signal.filtfilt(b, a, impulse)

# # Applies filter forward in time twice (for same frequency response)
# imp_lf = signal.lfilter(b, a, signal.lfilter(b, a, impulse))

# plt.subplot(2, 2, 1)
# plt.semilogx(20*np.log10(np.abs(rfft(imp_lf))))
# plt.ylim(-100, 20)
# plt.grid(True, which='both')
# plt.title('lfilter')

# plt.subplot(2, 2, 2)
# plt.semilogx(20*np.log10(np.abs(rfft(imp_ff))))
# plt.ylim(-100, 20)
# plt.grid(True, which='both')
# plt.title('filtfilt')

# sig = np.cumsum(randn(800))  # Brownian noise
# sig_ff = signal.filtfilt(b, a, sig)
# sig_lf = signal.lfilter(b, a, signal.lfilter(b, a, sig))
# plt.subplot(2, 1, 2)
# plt.plot(sig, color='silver', label='Original')
# plt.plot(sig_ff, color='#3465a4', label='filtfilt')
# plt.plot(sig_lf, color='#cc0000', label='lfilter')
# plt.grid(True, which='both')
# plt.legend(loc="best")
