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
                
        for i in range(height):
            for j in range(width):
                image_size_init = image_input.shape                     
                if bounding_box[0]+j >= image_size_init[1] or bounding_box[1]+i >= image_size_init[0]:
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

    



