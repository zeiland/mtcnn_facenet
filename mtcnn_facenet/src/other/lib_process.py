from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import tensorflow as tf
import pickle
import argparse
import numpy as np
from scipy import misc
import copy
from path_settings import *
import facenet
import compare_result


def completeLib() :

    filenames_jpg = os.listdir(LIB_PIC_DIR)
    filenames_pkl = os.listdir(LIB_PKL_DIR)

    s=set()
    for filename in filenames_pkl:
        filename=filename[0:-4]
        s.add(filename)
    for filename in filenames_jpg:
        filename=filename[0:-4]
        if(filename not in s):
            path_image=LIB_PIC_DIR+filename+'.jpg'
            inputstring=['20180408-102900',path_image,]
            temp_emb = getEmb(parseArguments(inputstring))
            pkl_filename = filename + ".pkl"
            print("updating lib_pkl :" + pkl_filename)
            output = open(LIB_PKL_DIR + pkl_filename , 'wb')     #create the target pkl_file in binary 
            pickle.dump(temp_emb , output , 2)                      #print emb value
            output.close()


def getEmb(args) :
    images = []
    for image_file in args.image_files:
            img = misc.imread(os.path.expanduser(image_file), mode='RGB')
            images.append(img)

    with tf.Graph().as_default():
        with tf.Session() as sess:
            # Load the model
            facenet.load_model(args.model)
    
            # Get input and output tensors
            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

            # Run forward pass to calculate embeddings
            feed_dict = { images_placeholder: images, phase_train_placeholder:False }
            emb = sess.run(embeddings, feed_dict=feed_dict)
    return emb                   #array of 1*512


def parseArguments(argv):
    parser = argparse.ArgumentParser()
    
    parser.add_argument('model', type=str, 
        help='Could be either a directory containing the meta_file and ckpt_file or a model protobuf (.pb) file')
    parser.add_argument('image_files', type=str, nargs='+', help='Images to compare')
    parser.add_argument('--image_size', type=int,
        help='Image size (height, width) in pixels.', default=160)
    parser.add_argument('--margin', type=int,
        help='Margin for the crop around the bounding box (height, width) in pixels.', default=44)
    parser.add_argument('--gpu_memory_fraction', type=float,
        help='Upper bound on the amount of GPU memory that will be used by the process.', default=1.0)
    return parser.parse_args(argv)

#lib_complete()
    
def complete_lib_weigh() :
    filenames_pkl = os.listdir(LIB_PKL_DIR)
    filenames_weigh = os.listdir(LIB_WEIGH_DIR)

    s=set()
    for filename in filenames_weigh:
        s.add(filename)
    for filename in filenames_pkl:
        if(filename not in s):
            same_person_pic=[filename,]
            for  another_every_pic_pkl in filenames_pkl:
                if((filename[:-5]==another_every_pic_pkl[:-5]) and (filename!=another_every_pic_pkl)):
                    same_person_pic.append(another_every_pic_pkl)
            if(len(same_person_pic)!=3):
                print(filename + "doesn't contain 3 pkl files")
                continue
            print("weigh lib completing: " + filename[:-6])
            compare_result.weigh_modify(same_person_pic[0] , same_person_pic[1] ,same_person_pic[2] , LIB_WEIGH_DIR)
        



