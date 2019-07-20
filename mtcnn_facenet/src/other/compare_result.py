import os,sys
import numpy as np
import pickle
from path_settings import *

def calculateDiff(pkl_file_1 , pkl_file_2) :
    with open(pkl_file_1 , 'rb') as f :
        binary_file_1 = pickle.load(f)
    with open(pkl_file_2 , 'rb') as f :
        binary_file_2 = pickle.load(f)
    dist = np.sqrt(np.sum(np.square(np.subtract(binary_file_1[0,:], binary_file_2[0,:]))))
    return dist



def compare():
    filenames_1=os.listdir(TEST_PKL_DIR)
    filenames_2=os.listdir(LIB_PKL_DIR)
    index=0
    ret = []
  

    for filename_1 in filenames_1:
#    print(i)
        index+=1
        min_diff=0.1
        aim_file='-'
        for filename_2 in filenames_2:
            diff = calculateDiff(TEST_PKL_DIR + filename_1,LIB_PKL_DIR + filename_2)
            if(diff < min_diff):
                min_diff = diff
                aim_file = filename_2
        if index==1:
            print("face\t\tmost_similar_face\tdifference")

        print ("%s\t\t%s\t\t%.3f"%(filename_1,aim_file,min_diff))


        if(aim_file!='-'):
            ret.append(aim_file)

    return ret
