import lib_process
import os
import pickle
from path_settings import *

def test_pkl_lib_add() :

    filenames_jpg = os.listdir(TEST_PIC_DIR)
    for filename in filenames_jpg :
        path_image = TEST_PIC_DIR + filename
        inputstring=['20180408-102900',
            path_image,]
        temp_emb = Lib_complete.getEmb(Lib_complete.parse_arguments(inputstring))
        pkl_filename = filename[0:-4] + ".pkl"
        output = open(TEST_PKL_DIR + pkl_filename , 'wb')     #create the target pkl_file in binary 
        pickle.dump(temp_emb , output , 2)                      #print emb value
        output.close()


