# -*- coding: utf-8 -*-
from math import fabs as fabs
from math import floor as floor
from math import sqrt as sqrt
from scipy.special import erfc as erfc
from scipy.special import gammaincc as gammaincc
from scipy.spatial.distance import hamming

import numpy as np

class FHD:
    
    @staticmethod
    def inter_array_FHD(array_1, array_2):
        """
        Parameters: array_1, array_2. Two binary arrays of matching length representing strings to have FHD compared.
        Returns: the Fractional (normalized) hamming distance between array_1 and array_2
        Notes: the function will flatten the arrays, so the format shouldn't matter - they can be input as m x n or mn x 1, for example
        """
        #flatten the arrays so that they have the same format
        flat_array_1 = array_1.flatten()
        flat_array_2 = array_2.flatten()
        
        #compute length of input data, needed for normalizing. check both arrays have same length.
        input_length = len(flat_array_1)
        if len(flat_array_2) != input_length:
            raise ValueError("Length Mismatch")

        #return FHD
        return hamming(flat_array_1, flat_array_2)
    
    def inter_array_FHD_test(devices, tested_index = 0):
        """
        Parameters
        ----------
        devices : Array
            Array of read values for each device.
        tested_index : Integer, optional
            DESCRIPTION. The index of the device to be tested. Default is the first device in devices.

        Returns
        -------
        p-value for the inter array FHD test for the indexed device 

        """
        no_of_devices = len(devices)
        device_length = len(devices[0].flatten())

        #makes a list of FHD scores for tested device against other devices
        FHD_scores = np.array([FHD.inter_array_FHD(devices[tested_index], devices[i]) 
                               for i in range(no_of_devices) if i != tested_index
                            ])
        
        #compute chi^2 statistic:
        squared_distances = (FHD_scores - 0.5) ** 2
        chi_squared = 4 * device_length * squared_distances.sum()
        
        #get p value using the incomplete gamma function
        p_value = gammaincc((no_of_devices - 1) / 2, chi_squared / 2)
        return p_value
        
    
    @staticmethod
    def FHD_values_serializer(devices):
        """
        Parameters
        ----------
        devices : Array
            Array of read values for each device.
        Returns
        -------
        array of FHD scores for the devices under test. 
        """
        no_of_arrays = len(devices)
        FHD_value_arrays = np.empty(no_of_arrays, dtype=object)
        for i in range(no_of_arrays):
            FHD_value_arrays[i] = FHD.inter_array_FHD_test(devices, tested_index = i)
        return FHD_value_arrays
                