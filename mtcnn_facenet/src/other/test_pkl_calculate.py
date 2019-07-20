import lib_process
import os
import pickle
from path_settings import *

def addPklLib() :
    filenames_jpg = os.listdir(TEST_PIC_DIR)
    print("detect ",len(filenames_jpg)," face(s)")
    index = 0
    for filename in filenames_jpg :
        index += 1
        print("calculating " , index , " embbing value")
        path_image = TEST_PIC_DIR + filename
        input_string=['20180408-102900',
            path_image,]
        temp_emb = lib_process.getEmb(lib_process.parseArguments(input_string))
        pkl_filename = filename[0:-4] + ".pkl"
        output = open(TEST_PKL_DIR + pkl_filename , 'wb')     #create the target pkl_file in binary 
        pickle.dump(temp_emb , output , 2)                      #print emb value
        output.close()


