import os,sys
import numpy as np
import pickle
from path_settings import *

def diff_calculate(pkl_file_1 , pkl_file_2) :
    with open(pkl_file_1 , 'rb') as f :
        binary_file_1 = pickle.load(f)
    with open(pkl_file_2 , 'rb') as f :
        binary_file_2 = pickle.load(f)
    dist = np.sqrt(np.sum(np.square(np.subtract(binary_file_1[0,:], binary_file_2[0,:]))))
    return dist



def compare():
    filenames1=os.listdir(TEST_PKL_DIR)
    filenames2=os.listdir(LIB_PKL_DIR)
    index=0
    ret = []
  

    for filename1 in filenames1:
#    print(i)
        index+=1
        min_diff=0.8
        aimfile='-'
        for filename2 in filenames2:
            diff = diff_calculate(TEST_PKL_DIR + filename1,LIB_PKL_DIR + filename2)
            if(diff < min_diff):
                min_diff = diff
                aimfile = filename2
        if index==1:
            print("face\t\tmost_similar_face\tdifference")

        print ("%s\t\t%s\t\t%.3f"%(filename1,aimfile,min_diff))


        if(aimfile!='-'):
            ret.append(aimfile)

    return ret
