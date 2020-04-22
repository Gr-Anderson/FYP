import numpy as np
from scipy.signal import argrelextrema


class Segment:
    """
    A segment is a section of an ECG signal between two neighbouring R-peaks

    ...
    
    Attributes
    ----------
    no_of_segments : int
        a int representing the number of segemnts to overlay
        
    Methods
    -------
    combining_segments()
        Combines multiple segments, overlayed on each other
    find_features_lower()
        Finds the lower unique features of a segment
    find_features_higher()
        Finds the higher unique features of a segment
    """

    no_of_segments = 5

    def __init__(self, bio_signal):
        """
        Parameters
        ----------
        bio_signal : BiometricSignal
            An ECG signal object
        combined_seg : numpy.ndarray
            Contains multiple segments overlayed on each other 
        features_lower() : tuple
            The lower side unique features of a segment
        features_higher() : tuple
            The higher side unique features of a segment
        """

        self.bio_signal = bio_signal
        self.combined_seg = self.combining_segments()
        self.features_lower = self.find_features_lower()
        self.features_higher = self.find_features_higher()

    def combining_segments(self):
        r"""Combines multiple segments, overlayed on one another

        This function combines multiple neighbouring R-peaks and overlays them
        to form a single segment. This an average over multiple segments.
                   
        Returns
        -------
        combined_seg : numpy.ndarray
            A numpy array containing multiple segments overlayed on one another
        """

        combined_seg_does_not_exist = True
        smallest_seg = None

        for i in range(0, self.no_of_segments):
            segment_start = self.bio_signal.r_peaks[0][i]
            segment_end = self.bio_signal.r_peaks[0][i + 1]

            extracted_segment = self.bio_signal.standardised_signal[
                segment_start:segment_end
            ]
            if smallest_seg == None:
                smallest_seg = len(extracted_segment)
            elif len(extracted_segment) < smallest_seg:
                smallest_seg = len(extracted_segment)

            if combined_seg_does_not_exist:
                # adds additional zeros to the end of the first segment
                # this is to prevent a crash as segments may have differnet lengths
                combined_seg = np.zeros(len(extracted_segment) + 100)
                combined_seg_does_not_exist = False
            for j in range(0, len(extracted_segment)):
                combined_seg[j] = combined_seg[j] + extracted_segment[j]

        combined_seg = np.trim_zeros(combined_seg)
        combined_seg = combined_seg[0:smallest_seg]
        return combined_seg

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

        features_lower = argrelextrema(self.combined_seg, np.less, order=5)
        self.features_lower = (features_lower[0], self.combined_seg[features_lower[0]])
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

        features_higher = argrelextrema(self.combined_seg, np.greater, order=5)
        self.features_higher = (
            features_higher[0],
            self.combined_seg[features_higher[0]],
        )
        return self.features_higher
