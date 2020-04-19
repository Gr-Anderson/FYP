class Segment:
    """
    A segment is a section of an ECG signal between two neighbouring R-peaks

    ...
    
    Attributes
    ----------
    no_of_segments -> int
        a int representing the number of segemnts to overlay
        
    Methods
    -------
    combining_segments()
        Combines multiple segments, overlayed on each other
    get_mean_of_segments()
        Finds the mean of multiple segments
    standardise_mean_segment()
        Standardises a mean segment for processing
    features_lower()
        The lower side unique features of a segment
    features_higher()
        The higher side unique features of a segment
    """
    
    no_of_segments = 5
    
    
    def __init__(self, bio_signal):
        """
        Parameters
        ----------
        bio_signal -> BiometricSignal
            An ECG signal object
        combined_seg -> numpy.ndarray
            Contains multiple segments overlayed on each other 
        mean_segment -> numpy.ndarray
            The result of combining multiple segments
        standardised_mean_segment -> numpy.ndarray
            Standareised mean segment, standisatin in nesscessary for processing
        """
        
        self.bio_signal = bio_signal
        self.combined_seg = self.combining_segments()
        self.mean_segment = self.get_mean_of_segments()
        self.standardised_mean_segment = self.standardise_mean_segment()
        self.features_lower = self.find_features_lower()
        self.features_higher = self.find_features_higher()


    def combining_segments(self):
        r"""Combines multiple segments, overlayed on each other

        This function combines multiple neighbouring R-peaks and overlays them
        to form a single segment. This is the first step in finding a mean
        segment.
                   
        Returns
        -------
        combined_seg -> numpy.ndarray
            A numpy array containing multiple segments overlayed on one another
        """
        
        combined_seg_does_not_exist = True
        smallest_seg = None
        
        for i in range (0, self.no_of_segments):
            segment_start = self.bio_signal.r_peaks[0][i]
            segment_end = self.bio_signal.r_peaks[0][i+1]

            extracted_segment = self.bio_signal.amended_signal[segment_start:segment_end]
            if smallest_seg == None:
                smallest_seg = len(extracted_segment)
            elif (len(extracted_segment) < smallest_seg):
                smallest_seg = len(extracted_segment)

            if combined_seg_does_not_exist:
                # adds additional zeros to the end of the first segment
                # this is to prevent a crash as segments may have differnet lengths
                combined_seg = np.zeros(len(extracted_segment) + 100)
                combined_seg_does_not_exist = False
            for j in range(0,len(extracted_segment)):
                combined_seg[j] =  combined_seg[j] + extracted_segment[j]
            
        combined_seg = np.trim_zeros(combined_seg)
        combined_seg = combined_seg[0:smallest_seg]
        return combined_seg
                

    def get_mean_of_segments(self):
        r"""Finds the mean of multiple segments

        This function finds the mean segment by looping through each element in
        the combined segment and dividing it by `no_of_segments`

        mean_segment -> numpy.ndarray
            A numpy array containing the mean segment of the combined segments
        """
        
        mean_segment = np.array([])
        
        for k in range (0, len(self.combined_seg)):
            mean_segment = np.append (mean_segment, self.combined_seg[k] / self.no_of_segments)
            
        return mean_segment

    
    def standardise_mean_segment(self):
        r"""Standardises a mean segment for processing

        This function is required because not all ECG signals don't start at zero. The
        lowest value is found and this is subtracted from every element in the
        mean segment.
            
        Returns
        -------
        standardised_mean_segment -> numpy.ndarray
            Standareised mean segment, standisatin in nesscessary for processing
        """        
        
        standardised_mean_segment = np.array([])
        
        min_of_mean_segment = min(self.mean_segment)
        for value in range(0, len(self.mean_segment)):
            standardised_mean_segment = np.append (standardised_mean_segment, self.mean_segment[value] - min_of_mean_segment)

        return standardised_mean_segment
    
    def find_features_lower(self):
        r"""Finds the lower unique features of a segment

        This function uses argrelextrema, part of SciPy. Argrelextrema
        calculates the relative extrema of data, this means it examines
        data at either side of a point on the segment to identify variation.
        When if finds broad variations between points, it considers it unique, 
        labels that point as a feature and stores it in a tuple.
            
        Returns
        -------
        features_lower : tuple
            A tuple containing the positions of lower unique features. 
        """
        
        features_lower = argrelextrema(self.mean_segment, np.less, order=5)
        self.features_lower = (features_lower[0],self.mean_segment[features_lower[0]])       
        return self.features_lower


    def find_features_higher(self):
        r"""Finds the higher unique features of a segment

        This function uses argrelextrema, part of SciPy. Argrelextrema
        calculates the relative extrema of data, this means it examines
        data at either side of a point on the segment to identify variation.
        When if finds broad variations between points, it considers it unique, 
        labels that point as a feature and stores it in a tuple.
            
        Returns
        -------
        features_higher : tuple
            A tuple containing the positions of higher unique features. 
        """
        
        features_higher = argrelextrema(self.mean_segment, np.greater, order=5)
        self.features_higher = (features_higher[0],self.mean_segment[features_higher[0]]) 
        return self.features_higher

     