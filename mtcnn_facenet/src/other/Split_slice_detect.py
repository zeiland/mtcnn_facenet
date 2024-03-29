import numpy as np
from PIL import Image
import os
import cv2
from path_settings import *


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
        
        #font=cv2.FONT_HERSHEY_SIMPLEX#使用默认字体
        #img=cv2.putText(im,'3',(0,40),font,1.2,(255,255,255),2)#添加文字，1.2表示字体大小，（0,40）是初始的位置，(255,255,255)表示颜色，2表示粗细

        for i in range(height):
            for j in range(width):                    
                if bounding_box[0]+j >= len(image_input[0]) or bounding_box[1]+i >= len(image_input):
                    continue
                img_blank[i][j] = image_input[bounding_box[1]+i][bounding_box[0]+j]
                image_input[bounding_box[1]+i][bounding_box[0]+j] = 0
        
        img_resize = cv2.resize(img_blank,(face_size,face_size))
        cv2.imwrite(TEST_PIC_DIR + str(number) + ".jpg", img_resize)   #set the path of saving faces, but no Chinese path





def detectSlice(img , detector , slice_num) :

    results = detector.detect_faces(img)
    saveFaces(results , img)
    
    #纵向分割图片
    if slice_num > 1 :
        image_size_init = img.shape     
        image_size  = [image_size_init[1] , image_size_init[0]]        #(width , height)
        slice_width = int(image_size[0] / slice_num)
        for i in range(slice_num - 1) :
            img_slice  = np.zeros((image_size[1],slice_width,3),np.uint8)
            for j in range(image_size[1]):
                for k in range(slice_width):
                    img_slice[j][k] = img[j][k + i * slice_width]
            results = detector.detect_faces(img_slice)
            saveFaces(results , img_slice)

            for j in range(image_size[1]):
                for k in range(slice_width):
                    img[j][k + i * slice_width] = img_slice[j][k]
        #剩余最右侧一块
        left_width = image_size[0] - (slice_num - 1) * slice_width
        img_slice = np.zeros((image_size[1],left_width,3),np.uint8)
        for j in range(image_size[1]):
            for k in range(left_width):
                img_slice[j][k] = img[j][k + (slice_num - 1) * slice_width]
        results = detector.detect_faces(img_slice)
        saveFaces(results , img_slice)

        for j in range(image_size[1]):
            for k in range(left_width):
                img[j][k + (slice_num - 1) * slice_width] = img_slice[j][k]

    


def printNum(detector , image_input) :
    number = 0
    results = detector.detect_faces(image_input)
    font=cv2.FONT_HERSHEY_SIMPLEX#使用默认字体
    for result in results:                           #detect faces and save the faces into test_jpg
        bounding_box = result['box']
        keypoints = result['keypoints']
        number += 1

        #cut out face


        height = bounding_box[3]
        width = bounding_box[2]
        
        cv2.rectangle(image_input,
              (bounding_box[0], bounding_box[1]),
              (bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),
              (0,155,255),
              2)

        image_input=cv2.putText(image_input,str(number),(bounding_box[0],bounding_box[1]),font,0.8,(255,255,255),2)#添加文字，1.2表示字体大小，（0,40）是初始的位置，(255,255,255)表示颜色，2表示粗细

        
    cv2.imwrite(DATA_DIR + "\\test.jpg", image_input)
    