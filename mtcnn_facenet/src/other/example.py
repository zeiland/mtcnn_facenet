#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from path_settings import *
from mtcnn import MTCNN
import numpy as np
import Split_slice_detect 
import cut_out_detect
from compare_result import compare
from lib_process import lib_complete
from test_pkl_calculate import test_pkl_lib_add
from PIL import Image
import cv2
import brightness_and_contrast

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)


#detector = MTCNN()

#lib_complete()                #complete pkl_file of face_lib when new faces add into lib

filename_external = os.listdir(TEST_FILE)
for i in range(len(filename_external)) :
    filename_internal = os.listdir(TEST_FILE + filename_external[i])
    for j in range(len(filename_internal)) :
        TEST_FILE_NAME = TEST_FILE + filename_external[i] + "\\" + filename_internal[j]
        print(TEST_FILE_NAME)
        #del_file(TEST_PIC_DIR)            #clear all saved test file before adding new file 
        #del_file(TEST_PKL_DIR)
        #image = cv2.imread(TEST_FILE_NAME)
        #results = detector.detect_faces(image)
        detect_face_num = len(os.listdir(TEST_PIC_DIR))



#亮度调整
#gamma = 0.8  #小于1变亮，大于1变暗
#image = brightness_and_contrast.brightness_mod(image , gamma)
#对比度调整
#enhance_fact = 1.5  #增强因子为0.0将产生纯灰色图像；为1.0将保持原始图像
#image = brightness_and_contrast.contrast(image , enhance_fact)

#cv2.imwrite('D:\\test1.jpg' , image)


#分块识别
#Split_slice_detect.slice_n_detect(image , detector , 1)
#Split_slice_detect.slice_n_detect(image , detector , 2)
#Split_slice_detect.slice_n_detect(image , detector , 3#

#截脸识别
#cut_out_detect.cut_out_saveFaces(results , image, detector)



#test_pkl_lib_add()            #complete pkl_file of test faces
#unpresent=compare()           #compare the pkl_file in lib and test
#for i in unpresent:
#    print(i)


