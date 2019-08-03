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

def weigh_modify(pkl_file_1 , pkl_file_2 , pkl_file_3 , weigh_filename) :
    
    with open(LIB_PKL_DIR+pkl_file_1 , 'rb') as f :
        binary_file_1 = pickle.load(f)
    with open(LIB_PKL_DIR+pkl_file_2 , 'rb') as f :
        binary_file_2 = pickle.load(f)
    with open(LIB_PKL_DIR+pkl_file_3 , 'rb') as f :
        binary_file_3 = pickle.load(f)
    diff_mat = abs(np.subtract(binary_file_1[:], binary_file_2[:]))
    weigh_0 = np.array(np.sum(diff_mat)/diff_mat[:]/512)    #除以512是为了让和的大小保持与原来一样，这样和没改过权重的pkl文件直接算差值也不会存在系数的差别
    #weigh_0 = np.array(1000*np.sum(diff_mat)/diff_mat[:]/np.sum(np.sum(diff_mat)/diff_mat[:]))

    diff_mat = abs(np.subtract(binary_file_1[:], binary_file_3[:]))
    weigh_1 = np.array(np.sum(diff_mat)/diff_mat[:]/512)

    diff_mat = abs(np.subtract(binary_file_2[:], binary_file_3[:]))
    weigh_2 = np.array(np.sum(diff_mat)/diff_mat[:]/512)

    weigh = np.array((weigh_0[:]+weigh_1[:]+weigh_2[:])/3)

    create_pkl(weigh_filename + pkl_file_1 , weigh)
    create_pkl(weigh_filename + pkl_file_2 , weigh)
    create_pkl(weigh_filename + pkl_file_3 , weigh)

def create_pkl(pkl_filename , temp_emb) :
            output = open(pkl_filename , 'wb')     #create the target pkl_file in binary 
            pickle.dump(temp_emb , output , 2)                      #print emb value
            output.close()

def compare_weigh():
    filenames_test=os.listdir(TEST_PKL_DIR)
    filenames_weigh=os.listdir(LIB_WEIGH_DIR)
    filenames_lib=os.listdir(LIB_PKL_DIR)
    index=0
    ret = []
    for filename1 in filenames_test:       
#    print(i)
        index+=1
        min_diff=5
        aimfile='-'
        for filename2 in filenames_weigh:
            #diff =calculateDiff(TEST_PKL_DIR + filename1,LIB_WEIGH_DIR + filename2)
            for filename3 in filenames_lib:
                if filename2 == filename3 :
                    diff=diff_weigh_cal(TEST_PKL_DIR+filename1,LIB_WEIGH_DIR+filename2,LIB_PKL_DIR+filename3)             
                    if(diff < min_diff):
                        min_diff = diff
                        aimfile = filename2
        if index==1:
            print("face\t\tmost_similar_face\tdifference")
        print ("%s\t\t%s\t\t%.3f"%(filename1,aimfile,min_diff))

def compare_three():
    filenames_1=os.listdir(TEST_PKL_DIR)
    filenames_2=os.listdir(LIB_PKL_DIR)
    index=0
    ret = []
    for filename_1 in filenames_1:
#    print(i)
        index+=1
        min_diff=0.5
        aim_file='-'
        for filename_2 in filenames_2:
            #print(filename_2[:-6])
            diff_sum = 0
            for filename_another in filenames_2 :
                if filename_2[:-6] == filename_another[:-6] :
                    diff = calculateDiff(TEST_PKL_DIR + filename_1,LIB_PKL_DIR + filename_2)
                    diff_sum += diff
            diff_average = diff_sum/3
            if(diff_average < min_diff):
                min_diff = diff_average
                aim_file = filename_2
        if index==1:
            print("face\t\tmost_similar_face\tdifference")

        print ("%s\t\t%s\t\t%.3f"%(filename_1,aim_file,min_diff))


        if(aim_file!='-'):
            ret.append(aim_file)

    return ret

def compare_three_weigh():
    filenames_test=os.listdir(TEST_PKL_DIR)
    filenames_weigh=os.listdir(LIB_WEIGH_DIR)
    filenames_lib=os.listdir(LIB_PKL_DIR)
    index=0
    ret = []
    for filename1 in filenames_test:       
#    print(i)
        index+=1
        min_diff=5
        aimfile='-'
        for filename2 in filenames_lib:
            diff_total = 0
            for filename_another in filenames_lib :
                if filename_another[:-6] == filename2[:-6] :
                    for filename3 in filenames_weigh:
                        if filename2 == filename3 :
                            diff=diff_weigh_cal(TEST_PKL_DIR+filename1,LIB_WEIGH_DIR+filename2,LIB_PKL_DIR+filename3)
                            diff_total += diff
            diff_average = diff_total/3
            if(diff_average < min_diff):
                min_diff = diff_average
                aimfile = filename2
        if index==1:
            print("face\t\tmost_similar_face\tdifference")
        print ("%s\t\t%s\t\t%.3f"%(filename1,aimfile,min_diff))