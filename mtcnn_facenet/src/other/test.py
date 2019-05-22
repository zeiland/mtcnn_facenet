#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from path_settings import *
from mtcnn import MTCNN
import numpy as np
import Split_slice_detect 
import cut_out_detect
from PIL import Image
import cv2
import brightness_and_contrast
import time

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


detector = MTCNN()
#method=0 : origin mtcnn   method=1 : split  method=2 : cut
def test(method) :
    with open(RESULT_FILE+str(method) , 'w') as data_txt :
        data_txt.write('photo_name' + ' ' + 'actual_fac_num' + ' ' + 'detect_face_num' + ' ' + 'detect_rate' + ' ' + 'detect_time' +  '\n')
    filename_external = os.listdir(TEST_FILE)
    detected_photo_num = 0
    total_photo_num = 0
    print_limit = 0.01
    total_actual_face_num = 0
    total_detect_face_num = 0

    dict = {}
    with open(FACE_NUM_LIST , 'rb') as face_num_file:
        lines = face_num_file.readlines()
        for i in range (0, len(lines), 2):
            dict[str(lines[i])[2 : -5]] = int(lines[i+1])

    for i in range(len(filename_external)) :    
        total_photo_num += len(os.listdir(TEST_FILE + filename_external[i]))


    for i in range(len(filename_external)) :
        filename_internal = os.listdir(TEST_FILE + filename_external[i])
        for j in range(len(filename_internal)) :
            TEST_FILE_NAME = TEST_FILE + filename_external[i] + "\\" + filename_internal[j]
            #print(TEST_FILE_NAME)
            del_file(TEST_PIC_DIR)            #clear all saved test file before adding new file 
            #del_file(TEST_PKL_DIR)


           
            photo_name =filename_external[i] + "/" + filename_internal[j]           
            actual_face_num = dict[photo_name]   #find the address of first char of photo_name
            

            image = cv2.imread(TEST_FILE_NAME)
            time_start=time.time()                              #timing start
            results = detector.detect_faces(image)           #detect face
            Split_slice_detect.saveFaces(results , image)
            time_end=time.time()                                #timing end
            time_total = round(time_end - time_start , 3)
            detect_face_num = len(os.listdir(TEST_PIC_DIR))

            detect_rate = round(detect_face_num/actual_face_num , 3)
            total_actual_face_num += actual_face_num
            total_detect_face_num += detect_face_num
            

            with open(RESULT_FILE+str(method) , 'a') as data_txt :
                data_txt.write(photo_name + ' ' + str(actual_face_num) + ' ' + str(detect_face_num)+ ' '+ str(detect_rate) + ' ' + str(time_total)+ '\n' )

            detected_photo_num += 1
            detected_rate = detected_photo_num/total_photo_num
            if detected_rate > print_limit :
                print("have detected " + str(round(detected_rate , 2)))
                print_limit += 0.01
    total_detect_rate = round(total_detect_face_num/total_actual_face_num , 3)
    with open(RESULT_FILE+str(method) , 'a') as data_txt :
        data_txt.write('total_actual_face_num '+ str(total_actual_face_num) + '\ntotal_detect_face_num ' + str(total_detect_face_num) + '\ntotal_detect_rate ' + str(total_detect_rate))


        


test()
