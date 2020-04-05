import pandas as pd
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

class Capture():
    pass

class Filter():
    

    b, a = signal.butter(4, 0.25, analog=False)

    data = pd.read_csv("./assets/subject_raw_ecg.csv")
    sig = data["voltage"]

    filtered_signal = signal.filtfilt(b, a, sig)
    
    plt.figure(num=None, figsize=(10, 5), dpi=80, facecolor="w", edgecolor="k")
    plt.plot(filtered_signal, color="#000000", linewidth=1)
    plt.axis('off')
    # plt.savefig("project_presentation.png", dpi=150, quality=100, bbox_inches='tight')
    plt.tight_layout()
    plt.show()

class RPeaks():
    pass

class Segment():
    pass
