import numpy as np

from FBG import FBG_process

def main():
    FBG_params_filename = './FBG_params.json'
    
    # create class by loading json file
    fbg_process = FBG_process.load_params(FBG_params_filename)
    
    # create class by init function
    # use calibration matrix in fbg_process1
    fbg_process2 = FBG_process(4,6,fbg_process.cal_mat)
    # print out attributs in fbg_process2
    print(fbg_process2.Num_CH)
    print(fbg_process2.Num_AA)
    print(fbg_process2.cal_mat)

    



if __name__ == "__main__":
    main()

