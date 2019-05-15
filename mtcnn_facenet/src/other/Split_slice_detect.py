import numpy as np
from PIL import Image
import os
import cv2
from path_settings import *
from mtcnn import MTCNN


def saveFaces(results , image_input):
    face_size = 160    
    number = len(os.listdir(TEST_PIC_DIR))
    for result in results:                           #detect faces and save the faces into test_jpg
        bounding_box = result['box']
        keypoints = result['keypoints']
        number += 1

        #cut out face
        img_blank = np.zeros((bounding_box[3], bounding_box[2], 3), np.uint8)
        img_resize = np.zeros((face_size,face_size,3),np.uint8)
        height = bounding_box[3]
        width = bounding_box[2]
                
        for i in range(height):
            for j in range(width):
                img_blank[i][j] = image_input[bounding_box[1]+i][bounding_box[0]+j]
                image_input[bounding_box[1]+i][bounding_box[0]+j] = 0
        
        img_resize = cv2.resize(img_blank,(face_size,face_size))
        cv2.imwrite(TEST_PIC_DIR + str(number) + ".jpg", img_resize)   #set the path of saving faces, but no Chinese path

def slice_2_detect(img) :
           #纵向分割图片
    slice_num = 2  
    image_size_2 = Image.open(TEST_FILE).size  #(width,height)
    slice_width = int(image_size_2[0] / slice_num)
    img_slice_left = np.zeros((image_size_2[1],slice_width,3),np.uint8)
    img_slice_right = np.zeros((image_size_2[1],image_size_2[0] - slice_width,3),np.uint8)
    for i in range(image_size_2[1]):
        for j in range(slice_width):
            img_slice_left[i][j] = img[i][j]
    for i in range(image_size_2[1]):
        for j in range(image_size_2[0] - slice_width):
            img_slice_right[i][j] = img[i][slice_width+j]
    #检测左侧和右侧图片
    detector = MTCNN()          #能否不重复出现
    results = detector.detect_faces(img_slice_left)
    saveFaces(results , img_slice_left)
    results = detector.detect_faces(img_slice_right)
    saveFaces(results , img_slice_right)

def slice_3_detect(img) :
           #纵向分割图片
    slice_num = 3
    image_size_3 = Image.open(TEST_FILE).size
    slice_width = int(image_size_3[0] / slice_num)
    img_slice_left  = np.zeros((image_size_3[1],slice_width,3),np.uint8)
    img_slice_mid   = np.zeros((image_size_3[1],slice_width,3),np.uint8)
    img_slice_right = np.zeros((image_size_3[1],image_size_3[0] - 2 * slice_width,3),np.uint8)
    for i in range(image_size_3[1]):
        for j in range(slice_width):
            img_slice_left[i][j] = img[i][j]
    for i in range(image_size_3[1]):
        for j in range(slice_width):
            img_slice_mid[i][j] = img[i][slice_width+j]
    for i in range(image_size_3[1]):
        for j in range(image_size_3[0] - 2 * slice_width):
            img_slice_right[i][j] = img[i][2 * slice_width+j]

    detector = MTCNN()          #能否不重复出现
    #检测左中右侧图片
    results = detector.detect_faces(img_slice_left)
    saveFaces(results , img_slice_left)
    results = detector.detect_faces(img_slice_mid)
    saveFaces(results , img_slice_mid)
    results = detector.detect_faces(img_slice_right)
    saveFaces(results , img_slice_right)
