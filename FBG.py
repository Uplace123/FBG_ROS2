"""
Created on Oct 4, 2022

This is a class file for process FBG rawdata

@author: Yangsheng XU
"""

import json
import os
import numpy as np

class FBG_process:

    def __init__( self, Num_CH: int, Num_AA: int, Calibration_matrix: dict ):
        self._Num_CH = Num_CH # channel number
        self._Num_AA = Num_AA # Active Area number
        self._cal_mat = Calibration_matrix # calibration matrix
        
        self.ref_wavelength = np.zeros(Num_CH * Num_AA)

    # __init__
    #properties

    @property
    def Num_CH( self ):
        return self._Num_CH

    @property
    def Num_AA( self ):
        return self._Num_AA
    @property
    def cal_mat( self ):
        return self._cal_mat

    @Num_AA.setter
    def Num_AA( self, num_AA: int):
        self._Num_AA = num_AA

    @Num_CH.setter
    def Num_CH( self, num_CH: int):
        self._Num_CH = num_CH
    
    
    @cal_mat.setter
    def cal_mat( self, Calibration_matrix: dict):
        self._cal_mat = Calibration_matrix


    #functions
    def get_curvatures( self, raw_signal: np.ndarray) -> np.ndarray:
        """
        calculate curvatures
        output: curvatures Num_AA * 2
        """


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

    







