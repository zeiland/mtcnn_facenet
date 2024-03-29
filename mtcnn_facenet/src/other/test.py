#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from path_settings import *
from mtcnn import MTCNN
import numpy as np
import split_slice_detect 
import cut_out_detect
from PIL import Image
import cv2
import brightness_and_contrast
import time
import compare_result
from lib_process import completeLib
from lib_process import complete_lib_weigh
from test_pkl_calculate import addPklTest
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



def test(method) :
    with open(RESULT_FILE[ : -4] + str(method) + '.txt' , 'w') as data_txt :
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
            dict[str(lines[i])[2 : -3]] = int(lines[i+1])

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
            if method == 0 :
                results = detector.detect_faces(image)           #detect face
                split_slice_detect.saveFaces(results , image)
            if method ==1 :
                split_slice_detect.detectSlice(image , detector , 3)
            if method == 2 :
                cut_out_detect.cutoutFaces(image, detector)
            time_end=time.time()                                #timing end
            time_total = round(time_end - time_start , 3)
            detect_face_num = len(os.listdir(TEST_PIC_DIR))

            detect_rate = round(detect_face_num/actual_face_num , 3)
            total_actual_face_num += actual_face_num
            total_detect_face_num += detect_face_num
            

            with open(RESULT_FILE[ : -4] + str(method) + '.txt' , 'a') as data_txt :
                data_txt.write(photo_name + ' ' + str(actual_face_num) + ' ' + str(detect_face_num)+ ' '+ str(detect_rate) + ' ' + str(time_total)+ '\n' )

            detected_photo_num += 1
            detected_rate = round(detected_photo_num/total_photo_num , 2)
            if detected_rate > print_limit :
                with open(PROGRESS , 'a') as progress_file :
                    progress_file.write(str(method) + " have detected " + str(detected_rate) + "\n")
                print_limit += 0.01
    total_detect_rate = round(total_detect_face_num/total_actual_face_num , 3)
    with open(RESULT_FILE[ : -4] + str(method) + '.txt' , 'a') as data_txt :
        data_txt.write('total_actual_face_num '+ str(total_actual_face_num) + '\ntotal_detect_face_num ' + str(total_detect_face_num) + '\ntotal_detect_rate ' + str(total_detect_rate))


def one_pic_detect() :
    del_file(TEST_PIC_DIR)
    image = cv2.imread(ONE_PIC_DETECT)
    results = detector.detect_faces(image)           #detect face
    split_slice_detect.saveFaces(results , image)
    print(len(os.listdir(TEST_PIC_DIR)))

def single_face_add_lib():
    files_path = DATA_DIR + "\\face_test\\pic_file\\"
    pic_file = os.listdir(files_path)
    for i in range(len(pic_file)) :
        #del_file(TEST_PIC_DIR)
        image = cv2.imread(files_path + pic_file[i])
        print(pic_file[i])
        results = detector.detect_faces(image)
        if (len(results) == 0) :
            print(pic_file[i] + ' cannot detect any face')
            continue
        face_size = 160    
        number = 0
        for result in results:                           #detect faces and save the faces into test_jpg
            bounding_box = result['box']
            keypoints = result['keypoints']
            number += 1
            img_blank = np.zeros((bounding_box[3], bounding_box[2], 3), np.uint8)
            img_resize = np.zeros((face_size,face_size,3),np.uint8)
            height = bounding_box[3]
            width = bounding_box[2]
                
            for k in range(height):
                for j in range(width):                    
                    if bounding_box[0]+j >= len(image[0]) or bounding_box[1]+k >= len(image):
                        continue
                    img_blank[k][j] = image[bounding_box[1]+k][bounding_box[0]+j]
                    image[bounding_box[1]+k][bounding_box[0]+j] = 0
            img_resize = cv2.resize(img_blank,(face_size,face_size))
            if number == 1 :
                cv2.imwrite(TEST_PIC_DIR + pic_file[i], img_resize) 
            else :
                cv2.imwrite(TEST_PIC_DIR + pic_file[i][:-4] + "_" + str(number) + ".jpg", img_resize) 


def gray_dectect() :
    files_path = DATA_DIR + "\\face_test\\pic_file\\"
    gray_path = DATA_DIR + "\\face_test\\gray\\"
    pic_file = os.listdir(files_path)
    face_size = 160
    for i in range(len(pic_file)) :
        #del_file(TEST_PIC_DIR)
        image_gray = cv2.imread(files_path + pic_file[i] , 0)
        image = cv2.imread(files_path + pic_file[i])
        cv2.imwrite(gray_path + pic_file[i],image_gray)
        image_gray = cv2.imread(gray_path + pic_file[i])

        print(pic_file[i])
        results = detector.detect_faces(image_gray)
        if (len(results) == 0) :
            print(pic_file[i] + ' cannot detect any face')
            continue
       
        number = 0

        for result in results:                           #detect faces and save the faces into test_jpg
            bounding_box = result['box']
            keypoints = result['keypoints']
            number += 1

            img_blank = np.zeros((bounding_box[3], bounding_box[2], 3), np.uint8)
            img_resize = np.zeros((face_size,face_size,3),np.uint8)
            height = bounding_box[3]
            width = bounding_box[2]
                
            for j in range(height):
                for k in range(width):                                       
                    img_blank[j][k] = image[bounding_box[1]+j][bounding_box[0]+k]
        
            img_resize = cv2.resize(img_blank,(face_size,face_size))
            if number == 1 :
                cv2.imwrite(TEST_PIC_DIR + pic_file[i], img_resize) 
            else :
                cv2.imwrite(TEST_PIC_DIR + pic_file[i][:-4] + "_" + str(number) + ".jpg", img_resize) 
        rect(image , results)

def rect(image , results):
    for result in results :
        bounding_box = result['box']
        cv2.rectangle(image,
              (bounding_box[0], bounding_box[1]),
              (bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),
              (0,155,255),
              1)
    cv2.imwrite(DATA_DIR+'\\face_test\\rect_pic.jpg' , image)


#del_file(TEST_PIC_DIR)
#del_file(TEST_PKL_DIR)
#del_file(LIB_WEIGH_DIR)
detector = MTCNN()
image = cv2.imread(DATA_DIR+'\\face_test\\pic_file\\lib_1.jpg')
split_slice_detect.printNum(detector,image)
#split_slice_detect.detectSlice(image , detector , 3)
##method=0 : origin mtcnn   method=1 : split  method=2 : cut
#with open(PROGRESS , 'w') as progress_file :
#    progress_file.write("start\n")
#single_face_add_lib()
#gray_dectect()
##test(0)
##test(1)
#test(2)
#del_file(LIB_WEIGH_DIR)
#completeLib()
#complete_lib_weigh()
#addPklTest()            #complete pkl_file of test faces
#unpresent=compare_result.compare()           #compare the pkl_file in lib and test
#unpresent = compare_result.compare_weigh()
#compare_result.compare_normal_distribution_exclude()
#compare_result.compare_three()
#for i in unpresent:
#    print(i)