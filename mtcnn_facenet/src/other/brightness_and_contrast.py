from skimage import data, exposure, img_as_ubyte , io
import matplotlib.pyplot as plt
import cv2
from path_settings import *
import numpy

from PIL import Image
from PIL import ImageEnhance
import os

def brightness_mod(image , gamma) :
    image= exposure.adjust_gamma(image, gamma)   #gamma>1 will be darker, gamma<1 will be brighter
    return image

def contrast(image , enhance_fact) :
    image = Image.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
    image = ImageEnhance.Contrast(image).enhance(enhance_fact)  #增强因子为0.0将产生纯灰色图像；为1.0将保持原始图像
    image = cv2.cvtColor(numpy.asarray(image),cv2.COLOR_RGB2BGR)
    return image


