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

#lib_complete()                #complete pkl_file of face_lib when new faces add into lib
with open(RESULT_FILE , 'w') as data_txt :
    data_txt.write('photo_name' + ' ' + 'actual_fac_num' + ' ' + 'detect_face_num' + ' ' + 'detect_rate' + ' ' + 'detect_time' +  '\n')
filename_external = os.listdir(TEST_FILE)
detected_photo_num = 0
total_photo_num = 0
print_limit = 0.01
for i in range(len(filename_external)) :    
    total_photo_num += len(os.listdir(TEST_FILE + filename_external[i]))

for i in range(len(filename_external)) :
    filename_internal = os.listdir(TEST_FILE + filename_external[i])
    for j in range(len(filename_internal)) :
        TEST_FILE_NAME = TEST_FILE + filename_external[i] + "\\" + filename_internal[j]
        #print(TEST_FILE_NAME)
        del_file(TEST_PIC_DIR)            #clear all saved test file before adding new file 
        #del_file(TEST_PKL_DIR)
        image = cv2.imread(TEST_FILE_NAME)
        time_start=time.time()                              #timing start
        results = detector.detect_faces(image)           #detect face
        Split_slice_detect.saveFaces(results , image)
        time_end=time.time()                                #timing end
        time_total = round(time_end - time_start , 3)
        detect_face_num = len(os.listdir(TEST_PIC_DIR))

        with open(FACE_NUM_LIST , 'rb') as face_num_file:
            file_context = face_num_file.read().decode('utf-8')
            photo_name = filename_external[i] + "/" + filename_internal[j]
            face_index = file_context.find(photo_name)   #find the address of first char of photo_name
            str_face_num = ''
            for k in range(2,6) :                        #k=1 is '\n', which is not need
                next_char = file_context[face_index + len(photo_name) + k]         
                if next_char == '\n' :
                    break
                str_face_num += next_char
        actual_face_num = int(str_face_num)
        detect_rate = round(detect_face_num/actual_face_num , 3)
        with open(RESULT_FILE , 'a') as data_txt :
            data_txt.write(photo_name + ' ' + str_face_num + ' ' + str(detect_face_num)+ ' '+ str(detect_rate) + ' ' + str(time_total)+ '\n' )

        detected_photo_num += 1
        detected_rate = detected_photo_num/total_photo_num
        if detected_rate > print_limit :
            print("have detected " + str(round(detected_rate , 2)))
            print_limit += 0.01

        
        


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


