from __future__ import division, print_function
import pandas as pd
import numpy as np
from numpy.random import randn
from numpy.fft import rfft
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

figure(num=None, figsize=(20, 10), dpi=80, facecolor="w", edgecolor="k")

b, a = signal.butter(4, 0.25, analog=False)

# Show that frequency response is the same
impulse = np.zeros(1000)
impulse[500] = 1

# Applies filter forward and backward in time
imp_ff = signal.filtfilt(b, a, impulse)

# sig = np.cumsum(randn(800))  # Brownian noise
data = pd.read_csv("test12.csv")
sig = data["voltage"]

sig_ff = signal.filtfilt(b, a, sig)

# plt.plot(sig, color="red", label="Original", linewidth=3)
# plt.plot(voltage, color="silver", label="Original")

plt.plot(sig_ff, color="#3465a4", label="filtfilt", linewidth=5)
plt.grid(True, which="both")


plt.savefig("test02.png")
plt.tight_layout()
plt.show()

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
