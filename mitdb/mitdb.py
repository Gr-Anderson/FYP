from IPython.display import display
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import wfdb

record = wfdb.rdrecord('mitdb/100', sampto=2000) 
wfdb.plot_wfdb(record=record, title='Record 100 from MIT-BIH Arrhythmia Database .dat form', figsize = (15,8)) 
display(record.__dict__)
