import csv

with open("test.csv", "r") as f:
    reader = csv.reader(f)
    your_list = list(reader)

print(your_list)

# from scipy import signal
# import matplotlib.pyplot as plt
# import numpy as np

# t = np.linspace(0, 1.0, 2001)
# xlow = np.sin(2 * np.pi * 5 * t)
# xhigh = np.sin(2 * np.pi * 250 * t)
# x = xlow + xhigh

# b, a = signal.butter(8, 0.125)
# y = signal.filtfilt(b, a, x, padlen=150)
# np.abs(y - xlow).max()

# b, a = signal.ellip(4, 0.01, 120, 0.125)  # Filter to be applied.
# np.random.seed(123456)

# n = 60
# sig = np.random.randn(n) ** 3 + 3 * np.random.randn(n).cumsum()

# fgust = signal.filtfilt(b, a, sig, method="gust")
# fpad = signal.filtfilt(b, a, sig, padlen=50)
# plt.plot(sig, "k-", label="input")
# plt.plot(fgust, "b-", linewidth=4, label="gust")
# plt.plot(fpad, "c-", linewidth=1.5, label="pad")
# plt.legend(loc="best")
# plt.show()

# import matplotlib.pyplot as plt  # For plotting
# from math import sin, pi  # For generating input signals
# import sys  # For reading command line arguments

# ### Filter - 6KHz->8Khz Bandpass Filter
# ### @param [in] input - input unfiltered signal
# ### @param [out] output - output filtered signal
# def filter(x):
#     y = [0] * 48000
#     for n in range(4, len(x)):
#         y[n] = (
#             0.0101 * x[n]
#             - 0.0202 * x[n - 2]
#             + 0.0101 * x[n - 4]
#             + 2.4354 * y[n - 1]
#             - 3.1869 * y[n - 2]
#             + 2.0889 * y[n - 3]
#             - 0.7368 * y[n - 4]
#         )
#     return y


# ###Read in desired frequency from command line
# frequency = int(sys.argv[1])

# ### Create empty arrays
# input = [0] * 48000
# output = [0] * 48000

# ### Fill array with xxxHz signal
# for i in range(48000):
#     input[i] = sin(2 * pi * frequency * i / 48000)  # + sin(2 * pi * 70 * i / 48000)

# ### Run the signal through the filter
# output = filter(input)

# ### Grab samples from input and output #1/100th of a second
# output_section = output[0:480]
# input_section = input[0:480]

# ### Plot the signals for comparison
# plt.figure(1)
# plt.subplot(211)
# plt.ylabel("Magnitude")
# plt.xlabel("Samples")
# plt.title("Unfiltered Signal")
# plt.plot(input_section)
# plt.subplot(212)
# plt.ylabel("Magnitude")
# plt.xlabel("Samples")
# plt.title("Filtered Signal")
# plt.plot(output_section)
# plt.show()
