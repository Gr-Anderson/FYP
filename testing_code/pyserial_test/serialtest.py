import matplotlib.pyplot as plt
import serial
import numpy

serial_data = serial.Serial('/dev/ttyACM1', 9600)

serial_list = []

while True:
    while (serial_data.inWaiting()==0):
        pass
    temp_string = serial_data.readline()
    serial_string = str(temp_string).replace("b", "").replace("'", "").replace("\\r", "").replace("\\n", "")
    serial_list.append(serial_string)
    plt.plot(serial_list)
    plt.ylabel('voltage')
    plt.xlabel('time')
    plt.show()
    
