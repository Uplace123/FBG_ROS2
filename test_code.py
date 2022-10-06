import numpy as np
import time
import os

from FBG import FBG_process
from sm130_interrogator_python.sm130_read import Interrogator

def main():
    FBG_params_filename = './FBG_params.json'
    

    """
    # create class by loading json file
    fbg_process = FBG_process.load_params(FBG_params_filename)
    # create class by init function
    # use calibration matrix in fbg_process1
    fbg_process2 = FBG_process(2,4,fbg_process.cal_mat)
    #fbg_process.__Num_CH = 100
    # print out attributs in fbg_process2
    print(fbg_process2.Num_CH)
    print(fbg_process2.Num_AA)
    print(fbg_process2.cal_mat)
    print(fbg_process2.ref_wavelength)
    """

    # test get realtime raw data and get curvatures
    interrogator = Interrogator("192.168.1.11",1852)
    refdata = interrogator.getData()
    
    fbg_process = FBG_process.load_params(FBG_params_filename)
    fbg_process.setRefdata(refdata)
    #os.system("pause")
    pause = input("enter anything to continue:")
    
    t = time.perf_counter()
    for i in range(10):

        rawdata = interrogator.getData()
        curvature = fbg_process.getCurvatures(rawdata)

        print(curvature)
        time.sleep(0.5)
    
    #end for
    print(f'cost time:{time.perf_counter() - t:.8f}s')



# main()

    



if __name__ == "__main__":
    main()

