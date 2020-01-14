import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# plt.style.use("fivethirtyeight")


data = pd.read_csv("test.csv")
voltage = data["voltage"]
line_numbers = []

for i in range(0, 676):
    line_numbers.append(i)

plt.plot(line_numbers, voltage)

plt.title("5 second ECG")
plt.ylabel("Voltage")
plt.xlabel("Line numbers")

plt.tight_layout()
plt.xticks(np.arange(0, 250, 10))

plt.grid(b=True, which="major", color="#666666", linestyle="-")

plt.show()
