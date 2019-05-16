from mtcnn.mtcnn import MTCNN
import numpy as np
from PIL import Image
import os
import cv2
from path_settings import *

def cut_out_saveFaces(results , image, detector):
    number = len(os.listdir(TEST_PIC_DIR))
    face_num = len(results)
    cut_column = []
    face_size = 160 
    image_size = [len(image[0]) , len(image)]
    for result in results:                           #detect faces and save the faces into test_jpg
        bounding_box = result['box']
        keypoints = result['keypoints']
        number += 1

        #cut out face
        img_blank = np.zeros((bounding_box[3], bounding_box[2], 3), np.uint8)
        img_resize = np.zeros((face_size,face_size,3),np.uint8)
        height = bounding_box[3]
        width = bounding_box[2]
        
        bounding_cut = bounding_box[0]            #保存检测到的脸所在的列数
        for i in range(width) :
            cut_column.append(bounding_cut)
            bounding_cut += 1
        

        for i in range(height):
            for j in range(width):
                img_blank[i][j] = image[bounding_box[1]+i][bounding_box[0]+j]
        
        face_num -= 1
        img_resize = cv2.resize(img_blank,(face_size,face_size))
        cv2.imwrite(TEST_PIC_DIR + str(number) + ".jpg", img_resize)   #set the path of saving faces, but no Chinese path
        
        if face_num == 0 :                                     #detect again after removing the faces detected before
            #排序并删除重复的列数
            cut_column.sort()
            column_count = 0
            column = 0
            for i in range(len(cut_column)) :
                if i == 0 :
                    column = cut_column[0]
                    continue               
                if cut_column[i] == column :
                      column = cut_column[i]
                      cut_column[i] = 0
                      column_count += 1
                else :
                    column = cut_column[i]
            for i in range(column_count) :
                cut_column.remove(0)
            
                                                                                                #取反集得到要保存的列数
            column_reserved = []
            for i in range(image_size[0]) :
                column_reserved.append(i)
            for i in range(len(cut_column)) :
                column_reserved.remove(cut_column[i])
                
                                                                                               #将图片对应保存的列数赋值到image_cut
            image_cut = np.zeros((image_size[1], len(column_reserved), 3), np.uint8)
            for i in range(len(column_reserved)) :               
                for j in range(image_size[1]) :
                    image_cut[j][i] = image[j][column_reserved[i]]
            #cv2.imwrite(TEST_PIC_DIR + "cut.jpg", image_cut)

                                                                                                #detect again in image_cut

            results_again = detector.detect_faces(image_cut)
            if len(results_again) == 0 :
                #print(number)
                break
            else :
                for i in range(image_size[1]):
                    for j in range(len(image_cut)):
                        image[i][j] = image_cut[i][j] 
                cut_out_saveFaces(results_again , image_cut , detector)
