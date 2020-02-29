# from IPython.display import display
import matplotlib.pyplot as plt
import numpy as np
# import os
# import shutil
import wfdb
from wfdb import processing


def peaks_hr(sig, peak_inds, fs, title):
    "Plot a signal with its peaks and heart rate"
    hrs = processing.compute_hr(sig_len=sig.shape[0], qrs_inds=peak_inds, fs=fs)
    
    N = sig.shape[0]
    
    fig, ax_left = plt.subplots(figsize=(10, 5))
    ax_right = ax_left.twinx()
    
    ax_left.plot(sig, color='#3979f0', label='Signal')
    ax_left.plot(peak_inds, sig[peak_inds], 'rx', marker='x', color='#8b0000', label='Peak', markersize=12)
    ax_right.plot(np.arange(N), hrs, label='Heart rate', color='m', linewidth=2)

    ax_left.set_title(title)

    ax_left.set_xlabel('Time (ms)')
    ax_left.set_ylabel('ECG (mV)', color='#3979f0')
    ax_right.set_ylabel('Heart rate (bpm)', color='m')
    ax_left.tick_params('y', colors='#3979f0')
    ax_right.tick_params('y', colors='m')
    plt.show()


record = wfdb.rdrecord('sampledata/100', sampfrom=0, sampto=2000, channels=[0])

qrs_inds = processing.gqrs_detect(sig=record.p_signal[:,0], fs=record.fs)

peaks_hr(record.p_signal, qrs_inds, record.fs, "GQRS peak detection on record 100")
    
min_bpm = 20
max_bpm = 230

search_radius = int(record.fs * 60 / max_bpm)
corrected_peak_inds = processing.correct_peaks(record.p_signal[:,0], peak_inds=qrs_inds,
                                               search_radius=search_radius, smooth_window_size=150)


print('Corrected gqrs detected peak indices:', sorted(corrected_peak_inds))
peaks_hr(sig=record.p_signal, peak_inds=sorted(corrected_peak_inds), fs=record.fs,
         title="Corrected GQRS peak detection on sampledata/100")


# from IPython.display import display
# import matplotlib.pyplot as plt
# import numpy as np
# import os
# import shutil
# import wfdb
# from wfdb import processing

# record = wfdb.rdrecord('mitdb/100', sampto=2000)
# annotation = wfdb.rdann('mitdb/100', 'atr', sampto=2000)

# wfdb.plot_wfdb(record=record, annotation=annotation, title='Record 100 from MIT-BIH Arrhythmia Database .dat form', figsize = (15,8)) 
# display(record.__dict__)
