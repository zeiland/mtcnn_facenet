import os
import sys


SYS_DIR = os.path.dirname(__file__) 
SYS_DIR = os.path.dirname(SYS_DIR)
sys.path.append(os.path.join(SYS_DIR,"mtcnn\\mtcnn"))
sys.path.append(os.path.join(SYS_DIR, "facenet"))

DATA_DIR = os.path.dirname(__file__)  
DATA_DIR = os.path.dirname(DATA_DIR)
DATA_DIR = os.path.dirname(DATA_DIR)
DATA_DIR = os.path.join(DATA_DIR,'data')

TEST_FILE = DATA_DIR + '\\face_picture\\zzzl.jpg'               #path of target file

TEST_PIC_DIR = DATA_DIR +'\\face_test\\jpg_file\\'   #path of the faces to solve

TEST_PKL_DIR = DATA_DIR + '\\face_test\\pkl_file\\'

LIB_PIC_DIR = DATA_DIR + '\\face_lib\\jpg_file\\'      #path of the lib face picture
 
LIB_PKL_DIR = DATA_DIR + '\\face_lib\\pkl_file\\'     #path of the lib pkl file 