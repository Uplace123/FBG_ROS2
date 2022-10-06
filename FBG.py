"""
Created on Oct 4, 2022

This is a class file for process FBG rawdata

@author: Yangsheng XU
"""

import json
import os
import numpy as np

class FBG_process:

    def __init__( self, num_CH: int, num_AA: int, calibration_matrix: dict ):
        self.Num_CH = num_CH # channel number
        self.Num_AA = num_AA # Active Area number
        self.cal_mat = calibration_matrix # calibration matrix
        """
        cal_mat: dict, {'AA1': [num_AA * 2], 'AA2':[num_AA * 2],...}
        """
        
        self.ref_wavelength = np.zeros(num_CH * num_AA).reshape(num_CH,num_AA)
        """
        ref_wavelength: ndarray,    CH1 AA1 AA2 AA3 ...
                                    CH2 AA1 AA2 AA3 ...
                                    ...
        """

    # __init__

    #properties
    

    #functions
    def getCurvatures( self, raw_signal: np.ndarray) -> np.ndarray:
        """
        calculate curvatures
        input: raw_signal, Num_CH * Num_AA
        output: curvatures, Num_AA * 2
        """
        curvatures = np.zeros(self.Num_AA*2).reshape(self.Num_AA,2)

        # assume the ref_wavelength has been updated
        # get difference between rawdata and refdata
        diff_value = raw_signal - self.ref_wavelength

        for i in range(self.Num_AA):
            AAi = np.array([diff_value[j,i] for j in range(self.Num_CH)])
            curvatures[[i],:]  = AAi @ self.cal_mat['AA'+str(i+1)]
        # end for

        return curvatures
    
    def setRefdata(self,reference_wavelength:np.ndarray):
        self.ref_wavelength = reference_wavelength
    # end setRefdata


        


        


        # todo
    
    @staticmethod
    def load_params( filename: str):
        """
        load a FBG_process class from a saved Json file
        return a FBG_process class
        """
        with open( filename, 'r') as json_file:
            content = json.load( json_file )
        

        cal_mats = { }
        #Num_CH = content.get("# channels",None)
        #Num_AA = content.get("# active areas",None)

        if "Calibration Matrix" in content.keys():
            """
            form:
            {"AA1" : np.ndarray Num_CH * 2, "AA2" : np.ndarray ...}
            """

            for AAnames,calvalues in content["Calibration Matrix"].items():
                cal_mats[AAnames] = np.array(calvalues)
            # end for
        
        # end if
    
        fbg_process = FBG_process(content["# channels"], content["# active areas"], cal_mats)

        return fbg_process
    # load_params

    







