import numpy as np

class Segment:

    
    def __init__(self, bio_signal):
        self.bio_signal = bio_signal
        self.combined_seg = self.combining_segments()
        self.mean_segment = self.get_mean_of_segments()
        self.standardised_mean_segment = self.standardise_mean_segment()

# ----------------------------------------------------
# --------------Combining Segments -------------------
# ----------------------------------------------------
    def combining_segments(self):
        combined_seg_does_not_exist = True
        smallest_seg = None
        
        for i in range (0, 5):
            segment_start = self.bio_signal.r_peaks[0][i]
            segment_end = self.bio_signal.r_peaks[0][i+1]

            extracted_segment = self.bio_signal.amended_signal[segment_start:segment_end]
            if smallest_seg == None:
                smallest_seg = len(extracted_segment)
            elif (len(extracted_segment) < smallest_seg):
                smallest_seg = len(extracted_segment)

            if combined_seg_does_not_exist:
                combined_seg = np.zeros(len(extracted_segment) + 100)
                combined_seg_does_not_exist = False
            for j in range(0,len(extracted_segment)):
                combined_seg[j] =  combined_seg[j] + extracted_segment[j]
            
        combined_seg = np.trim_zeros(combined_seg)
        combined_seg = combined_seg[0:smallest_seg]
        return combined_seg
                

    def get_mean_of_segments(self):

        mean_segment = np.array([])
        
        for k in range (0, len(self.combined_seg)):
            mean_segment = np.append (mean_segment, self.combined_seg[k] / 5)
            
        return mean_segment

    
    def standardise_mean_segment(self):

        standardised_mean_segment = np.array([])
        
        min_of_mean_segment = min(self.mean_segment)
        for value in range(0, len(self.mean_segment)):
            standardised_mean_segment = np.append (standardised_mean_segment, self.mean_segment[value] - min_of_mean_segment)

        return standardised_mean_segment

# END OF SEGMENT CLASS