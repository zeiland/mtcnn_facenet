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

def diff_weigh_cal(pkl_file_test ,weigh , pkl_file_lib) :
    with open(pkl_file_test , 'rb') as f :
        binary_file_test = pickle.load(f)
    with open(weigh , 'rb') as f :
        binary_file_weigh = pickle.load(f)
    with open(pkl_file_lib , 'rb') as f :
        binary_file_lib = pickle.load(f)
    binary_file_1 = np.abs(np.subtract(binary_file_test[:] , binary_file_lib[:]))    
    #binary_file_2 = np.multiply(binary_file_lib[:] , binary_file_weigh[:])
    dist = np.sqrt(np.sum(np.square(np.multiply(binary_file_1[:], binary_file_weigh[:]))))
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

def weith_modify(pkl_file_1 , pkl_file_2 , pkl_file_3 , weigh_filename) :
    with open(pkl_file_1 , 'rb') as f :
        binary_file_1 = pickle.load(f)
    with open(pkl_file_2 , 'rb') as f :
        binary_file_2 = pickle.load(f)
    with open(pkl_file_3 , 'rb') as f :
        binary_file_3 = pickle.load(f)
    diff_mat = abs(np.subtract(binary_file_1[:], binary_file_2[:]))
    weigh_0 = np.array(np.sum(diff_mat)/diff_mat[:]/512)    #除以512是为了让和的大小保持与原来一样，这样和没改过权重的pkl文件直接算差值也不会存在系数的差别

    diff_mat = abs(np.subtract(binary_file_1[:], binary_file_3[:]))
    weigh_1 = np.array(np.sum(diff_mat)/diff_mat[:]/512) 

    diff_mat = abs(np.subtract(binary_file_2[:], binary_file_3[:]))
    weigh_2 = np.array(np.sum(diff_mat)/diff_mat[:]/512)

    weigh = np.array((weigh_0[:]+weigh_1[:]+weigh_2[:])/3)
    #for i in range(512) :
    #    if weigh[i] > 1.1 :
    #        weigh[i] = 1.1
    #    if weigh[i] < 0.9 :
    #        weigh[i] = 0.9

    #dist = np.sqrt(np.sum(np.square(np.subtract(np.multiply(binary_file_1[0,:],weigh[:]), np.multiply(binary_file_2[0,:],weigh[:])))))
    #print(dist)
    #binary_file_1 = np.multiply(binary_file_1[:],weigh[:])
    #binary_file_2 = np.multiply(binary_file_2[:],weigh[:])
    create_pkl(weigh_filename + pkl_file_1[21 : ] , weigh)
    create_pkl(weigh_filename + pkl_file_2[21 : ] , weigh)
    create_pkl(weigh_filename + pkl_file_3[21 : ] , weigh)

def create_pkl(pkl_filename , temp_emb) :
            output = open(pkl_filename , 'wb')     #create the target pkl_file in binary 
            pickle.dump(temp_emb , output , 2)                      #print emb value
            output.close()


#pkl_file_1 = "D:\\face_lib\\pkl_file\\" + "zz1_lib.pkl"
#pkl_file_2 = "D:\\face_lib\\pkl_file\\" + "zz2_lib.pkl"
#pkl_file_3 = "D:\\face_lib\\pkl_file\\" + "zz3_lib.pkl"
#weith_modify(pkl_file_1 , pkl_file_2 , pkl_file_3 , LIB_WEIGH_DIR)

#test_face = "D:\\face_lib\\pkl_file\\" + "zl3_lib.pkl"

#lib_file = os.listdir(LIB_WEIGH_DIR)
#for i in range(len(lib_file)) :
#    dist = diff_weigh_cal(test_face , LIB_WEIGH_DIR + lib_file[i] , LIB_PKL_DIR + lib_file[i])
#    print(lib_file[i])
#    print(dist)
#print("\n")

#lib_file = os.listdir(LIB_PKL_DIR)
#for i in range(len(lib_file)) :
#    dist = diff_calculate(test_face , LIB_PKL_DIR + lib_file[i])
#    print(lib_file[i])
#    print(dist)