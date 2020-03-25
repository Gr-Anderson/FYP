import serial

import matplotlib.pyplot as plt

import time

serial_data = serial.Serial("/dev/ttyACM1", 9600)

serial_list = []


def capture_signal():
    # time in seconds to capture the ecg signal
    capture_time = 10

    t_end = time.time() + capture_time
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


def output_signal_to_csv():
    with open("subject_d.csv", "w") as ecg_file:
        ecg_file.write("voltage,\n")
        for item in serial_list:
            ecg_file.write("%s,\n" % item)
        ecg_file.write("0,")


capture_signal()
output_signal_to_csv()
