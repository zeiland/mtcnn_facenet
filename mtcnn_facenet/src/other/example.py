#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append("D:\\VS2017\\source\\repos\\mtcnn_facenet\\mtcnn_facenet\\src\\mtcnn\\mtcnn")
sys.path.append("D:\\VS2017\\source\\repos\\mtcnn_facenet\\mtcnn_facenet\\src\\facenet")

import numpy as np
import Split_slice_detect 
import cut_out_detect
from compare_result import compare
from Lib_complete import lib_complete
from test_pkl_calculate import test_pkl_lib_add
from path_settings import *
from PIL import Image
import cv2
from mtcnn import MTCNN


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


del_file(TEST_PIC_DIR)            #clear all saved test file before adding new file 
del_file(TEST_PKL_DIR)
lib_complete()                #complete pkl_file of face_lib when new faces add into lib


detector = MTCNN()
image = cv2.imread(TEST_FILE)
results = detector.detect_faces(image)
#分块识别
#Split_slice_detect.saveFaces(results , image)
#Split_slice_detect.slice_2_detect(image)
#Split_slice_detect.slice_3_detect(image)

#截脸识别
cut_out_detect.cut_out_saveFaces(results , image)

#test_pkl_lib_add()            #complete pkl_file of test faces
#unpresent=compare()           #compare the pkl_file in lib and test
#for i in unpresent:
#    print(i)


