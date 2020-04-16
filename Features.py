from scipy.signal import argrelextrema
import numpy as np

class Features:
    
    
    def __init__(self, mean_segment):
        self.mean_segment = mean_segment
        self.features_lower = self.find_features_lower()
        self.features_higher = self.find_features_higher()
        

    def find_features_lower(self):
        features_lower = argrelextrema(self.mean_segment, np.less, order=5)
        self.features_lower = (features_lower[0],self.mean_segment[features_lower[0]])       
        return self.features_lower


    def find_features_higher(self):
        features_higher = argrelextrema(self.mean_segment, np.greater, order=5)
        self.features_higher = (features_higher[0],self.mean_segment[features_higher[0]]) 
        return self.features_higher