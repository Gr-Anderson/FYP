class BiometricSignal: 
    """
    A class used to represent an ECG signal

    ...

    Attributes
    ----------
    captured_signal_csv : str
        a string representing a path to a csv file

    Methods
    -------
    capture_signal()
        Captures an ECG signal with an Arduino and AD8232
    output_signal_to_csv()
        Outputs the signal captured to a csv name in 'captured_signal_csv'
    filter_captured_signal(sound=None)
        Filters the ECG to reduce noise
    amend_signal(filtered_signal)
        Removes start and end of signal which are usually very noisy
    find_r_peaks(amended_signal)
        Finds the R-peaks in the signal
    """
    
    captured_signal_csv = "./assets/subject_raw_ecg.csv"
#     captured_signal_csv = "./subject2.csv"
#     captured_signal_csv = "./subject3a.csv"

    def __init__(self):
        """
        Parameters
        ----------
        captured_ecg : list
            List containing the ECG captured by the Arduino and AD8232
        filtered_signal : numpy.ndarray
            The signal with most of the noise removed
        amended_signal : numpy.ndarray
            The signal with the start and the end removed
        r_peaks : tuple
            Contains the positions of the R-peaks in the signal
        """
        
        self.captured_ecg = []
        self.filtered_signal = np.ndarray([])
        self.amended_signal = np.ndarray([])
        self.r_peaks = ()
        
        
    def capture_signal(self):
        r"""Captures ECG signal from Arduino and AD8232.

        This function captures an ECG signal with an Arduino and AD8232
        on port specified in `serial_data`. Before it begins capturing,
        there is a delay (set by `start_delay`) to allow the user to
        sit still. After this delay it will capture the ECG signal for
        the time specified in `capture_time`. The ECG signal will be
        assigned to the list `self.captured_ecg`.

        Variables
        ----------
        serial_data : serial.serialposix.Serial
            Specify the port to capture serial data on

        """
        
        serial_data = serial.Serial("/dev/ttyACM1", 9600)
        capture_time = 5
        t_end = time.time() + capture_time
        start_delay = 2

        time.sleep(start_delay)

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
                self.captured_ecg.append(int(serial_string))
#         return self.captured_ecg


    def output_signal_to_csv(self):
        r"""Captures ECG signal from Arduino and AD8232.

        This function captures an ECG signal with an Arduino and AD8232
        on port specified in `serial_data`. Before it begins capturing,
        there is a delay (set by `start_delay`) to allow the user to
        sit still. After this delay it will capture the ECG signal for
        the time specified in `capture_time`. `t_end` calcualtes the
        time it should stop capturing

        Parameters
        ----------
        sound : str, optional
            The sound the animal makes (default is None)

        Returns
        ------
        NotImplementedError
            If no sound is set for the animal or passed in as a
            parameter.
        """
        
        with open(BiometricSignal.captured_signal_csv, "w") as ecg_file:
            ecg_file.write("voltage,\n")
            for item in self.captured_ecg:
                ecg_file.write("%s,\n" % item)
            ecg_file.write("0,")


    def filter_captured_signal(self):
        numerator, denominator = signal.butter(4, 0.25, analog=False)
        data = pd.read_csv(BiometricSignal.captured_signal_csv)
        sig = data["voltage"]
        self.filtered_signal = signal.filtfilt(numerator, denominator, sig)
        return self.filtered_signal
    
    def amend_signal(self, filtered_signal):
#         threshold = 400
        start = 100
        end = -100
        self.amended_signal = filtered_signal[start:end]
        return self.amended_signal
    
    def find_r_peaks(self, amended_signal):
        """This is the summary line

        This is the further elaboration of the docstring. Within this section,
        you can elaborate further on details as appropriate for the situation.
        Notice that the summary and the elaboration is separated by a blank new
        line.
        """
        
        threshold = 400
#         start = 100
#         end = -100
        
#         amended_signal = amend_signal(filtered_signal)
        no_of_rows = amended_signal.shape[0]
        line_numbers = []
        theVoltage = []


        for i in range(0, no_of_rows):
            if amended_signal[i] > threshold:
                theVoltage.append(amended_signal[i])
            else:
                theVoltage.append(0)
            line_numbers.append(i)    


        ecg_plot = np.concatenate((theVoltage, line_numbers))

        self.r_peaks = argrelextrema(ecg_plot, np.greater, order=5)
        
        return self.r_peaks
