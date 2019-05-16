from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import tensorflow as tf
import facenet
import pickle
import argparse
import numpy as np
from scipy import misc
import copy
from path_settings import *




def lib_complete() :

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
            temp_emb = getEmb(parse_arguments(inputstring))
            pkl_filename = filename + ".pkl"
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


def parse_arguments(argv):
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
    
