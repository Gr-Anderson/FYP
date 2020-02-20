import csv
import time
import serial

serial_data = serial.Serial("/dev/ttyACM1", 9600)

serial_list = []

x_value = 0
total_1 = 1000
total_2 = 1000

fieldnames = ["x_value", "total_1"]

with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:

    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "x_value": x_value,
            "total_1": total_1,
        }

        csv_writer.writerow(info)

        x_value += 1
#         total_1 = total_1 + random.randint(-6, 8)
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
            total_1 = serial_string