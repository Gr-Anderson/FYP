class BiometricSignal: 
    """
    A class used to represent an ECG signal

    ...

    Attributes
    ----------
    captured_signal_csv -> str
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
        captured_ecg -> list
            List containing the ECG captured by the Arduino and AD8232
        filtered_signal -> numpy.ndarray
            The signal with most of the noise removed
        amended_signal -> numpy.ndarray
            The signal with the start and the end removed
        r_peaks -> tuple
            Contains the positions of the R-peaks in the signal
        """
        
        self.captured_ecg = []
        self.filtered_signal = np.ndarray([])
        self.amended_signal = np.ndarray([])
        self.r_peaks = ()
        
        
    def capture_signal(self):
        r"""Captures ECG signal from Arduino and AD8232.

        This function captures an ECG signal with an Arduino and AD8232
        on the port specified in `serial_data`. Before it begins capturing,
        there is a small delay (e.g. 2 seconds) to allow the user to get
        comfortable. After this delay it will capture the ECG signal and
        assign it to the list `self.captured_ecg`.
        
        Parameters
        ----------
        serial_data -> serial.serialposix.Serial, optinal
            Identifies the port to record the ECG signal, default is
            serial.Serial("/dev/ttyACM2", 9600)
        capture_time -> int, optional
            Time in seconds to capture ECG signal for, default is 5 
        start_delay -> numpy.ndarray
            Time in seconds to delay before recording starts, default is 2

        """
        
        t_end = time.time() + capture_time
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
        
        r"""Coverts `self.captured_ecg` to a csv

        This function converts the list `self.captured_ecg` to a csv and
        saves it to the location set in `captured_signal_csv`.
        
        """
        
        with open(BiometricSignal.captured_signal_csv, "w") as ecg_file:
            ecg_file.write("voltage,\n")
            for item in self.captured_ecg:
                ecg_file.write("%s,\n" % item)
            ecg_file.write("0,")


    def filter_captured_signal(self):
        
        r"""Reduces noise in the signal.

        Reduces noise which in picked up when recording an ECG signal.
        It uses a Butterworth filter to remove jagged parts of the signal
        and smoothen it give a more truer represtation of the ECG signal.
        
        Returns
        -------
        self.filtered_signal -> numpy.ndarray
            A filtered version of the captured ECG signal 

        """
            
        numerator, denominator = signal.butter(4, 0.25, analog=False)
        data = pd.read_csv(BiometricSignal.captured_signal_csv)
        sig = data["voltage"]
        self.filtered_signal = signal.filtfilt(numerator, denominator, sig)
        return self.filtered_signal
    
    def amend_signal(self, start = 100, end = -100):
        r"""Removes the begining and end of a filtered signal

        Sometimes there can be a lot of noise at the start and of a ECG
        signal which the `filter_captured_signal` function is unable to remove.
        The noise is caused by connecting to and from the capture device. This
        function takes care of that of that noise by removing the start and end of
        the captured ECG signal.
        
        Parameters
        ----------
        start -> int, optinal
            The position to start the clip the ECG signal from, default is 100
        end -> int, optional
            The position to end the clip of the ECG signal, default is 100
            
        Returns
        -------
        self.amended_signal -> numpy.ndarray
            An ammended version of `filtered_signal` 
            
        """
             
        self.amended_signal = self.filtered_signal[start:end]
        return self.amended_signal
    
    def find_r_peaks(self, threshold = 400):

        r"""Finds the R-peaks in an amended signal

        This function finds the R-peaks in an amended signal. R-peaks are 
        the highest part of a signal so it uses a threshold to illimitate lower
        unnesscary features which may be picked up as a false positive. 
        
        Parameters
        ----------
        threshold -> int, optinal
            The position to start looking for R-peaks from, default is 400
            
        Returns
        -------
        self.r_peaks -> tuple
            A tuple containing the positions of the R-peaks 
            
        """
        
        no_of_rows = self.amended_signal.shape[0]
        line_numbers = []
        theVoltage = []


        for i in range(0, no_of_rows):
            if self.amended_signal[i] > threshold:
                theVoltage.append(self.amended_signal[i])
            else:
                theVoltage.append(0)
            line_numbers.append(i)    


        ecg_plot = np.concatenate((theVoltage, line_numbers))

        self.r_peaks = argrelextrema(ecg_plot, np.greater, order=5)
        
        return self.r_peaks