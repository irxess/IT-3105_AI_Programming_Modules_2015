__author__ = 'keithd'

# Copied (and modified) from http://g.sweyla.com/blog/2012/mnist-numpy/, which is
# adapted from http://abel.ee.ucla.edu/cvxopt/_downloads/mnist.py

import os, struct
import time
from array import array as pyarray
import matplotlib.pyplot as pyplot
import numpy
import pickle

# The reduce function was removed in Python 3.0, so just use this handmade version.
def kd_reduce(func,seq):
    res = seq[0]
    for item in seq[1:]:
        res = func(res,item)
    return res

# Set this to the complete path to your mnist files.
## __mnist_path__ = "path/to/all/your/mnist/files"
__mnist_path__ = "/Users/keithd/core/python/data/mnist/basics/"

# The load_mnist function is the main interface between the MNIST files and your machine-learning code.  It fetches
# subsets of the entire training or test sets, as determined by the 'digits'
# argument.  For example, when digits = [5,8], this returns all and only the images of 5's and 8's.

# Note that the 'path' argument is the complete file path to the directory in which you
# store the 4 -ubyte files.  To test if this works, load this module and then type: "show_avg_digit(3)", which
# should produce a picture of the "average 3" in the training set.

# Also note that the training and test data are divided into two pairs of files.  Each pair contains the
# images and the labels, each in a separate file.  The functions in this file maintain that same distinction, always
# dealing with separate lists (or arrays) of images or labels.  Your own code may package a case into a combination of a feature
# vector and a label, but that is not done here.

# The representations created by load_mnist are:
# 1) images (i.e. features) - A 3-dimensional numpy array, where the first dimension is the index of the image in the
# subset, and the remaining two dimensions are those of the rows and columns of each image.
# 2) labels - a 2-dimensional numpy array whose first dimension is the number of images in subset and whose second
# dimension is always 1.   Check it out by calling and examining the results.

def load_mnist(dataset="training", digits=numpy.arange(10), path= __mnist_path__):

    if dataset == "training":
        fname_img = os.path.join(path, 'train-images.idx3-ubyte')
        fname_lbl = os.path.join(path, 'train-labels.idx1-ubyte')
    elif dataset == "testing":
        fname_img = os.path.join(path, 't10k-images.idx3-ubyte')
        fname_lbl = os.path.join(path, 't10k-labels.idx1-ubyte')
    else:
        raise ValueError("dataset must be 'testing' or 'training'")

    flbl = open(fname_lbl, 'rb')
    magic_nr, size = struct.unpack(">II", flbl.read(8))
    lbl = pyarray("b", flbl.read())
    flbl.close()

    fimg = open(fname_img, 'rb')
    magic_nr, size, rows, cols = struct.unpack(">IIII", fimg.read(16))
    img = pyarray("B", fimg.read())
    fimg.close()

    ind = [ k for k in range(size) if lbl[k] in digits ]
    N = len(ind)

    images = numpy.zeros((N, rows, cols), dtype=numpy.uint8)
    labels = numpy.zeros((N, 1), dtype=numpy.int8)
    for i in range(len(ind)):
        images[i] = numpy.array(img[ ind[i]*rows*cols : (ind[i]+1)*rows*cols ]).reshape((rows, cols))
        labels[i] = lbl[ind[i]]

    return images, labels

# *****   Viewing images *******
#  These two functions assume that the image is in the standard MNIST format: a 2-d numpy array.

# Other colormaps: binary, jet, copper, rainbow, summer, autumn, winter, spring...
def show_avg_digit(digit, cm = 'gray'):
    images, labels = load_mnist('training', digits=[digit])
    show_digit_image(images.mean(axis=0),cm=cm)

def show_digit_image(image,cm='gray'):
    pyplot.ion()
    pyplot.figure()
    pyplot.imshow(image, cmap=pyplot.get_cmap(cm))

# *** Image Conversion ****
# Conversions from arrays to (flat) lists, and the opposite conversion, called 'reconstruction'.

def flatten_image(image_array):
    def flatten(a,b): return a + b
    return kd_reduce(flatten, image_array.tolist())

def reconstruct_image(flat_list,dims=(28,28)):
    image = numpy.array(flat_list)
    image = numpy.reshape(image,dims)
    return image

# **** FLATTENING and RECONSTRUCTING CASES (images + labels)

# This converts each case into a vector of features (length = 28 x 28 = 784) and a class (0-9).  The
# two returned lists are of the 784-integer vectors and the labels.  If cases are sent in as an argument, then
# they are assumed to have the same format as that returned by load_mnist:  (list-of-images, list-of-labels)

def gen_flat_cases(digits=numpy.arange(10),type='training',cases=None):
     images, labels = cases if cases else load_mnist(type, digits=digits)
     i2 = list(map(flatten_image,images))
     l2 = kd_reduce((lambda a, b: a + b), labels.tolist())
     return i2, l2

def reconstruct_flat_cases(cases,dims=(28,28),nested=True):
    labels = numpy.array([[label] for label in cases[1]]) if nested else cases[1]
    images = [reconstruct_image(i,dims=dims) for i in cases[0]] if nested else cases[0]
    return images,labels

# ***** PICKLING FLAT CASES ********
# This uses pickle to dump cases to and retrieve cases from a binary file.

# In python3, you need the "b" after the "w" and the "r" in write/read mode.... indicating that we're writing bytes.
# Cases = pair: (all-images, all-labels)
def dump_flat_cases(filename,cases,dir=__mnist_path__,labeled=True):
    f = open(dir + filename,'wb')
    labels = cases[1] if labeled else numpy.ones(len(cases)) * -1  # -1 = no-label indicator
    pickle.dump([cases[0],labels],f)

def load_flat_cases(filename,dir=__mnist_path__):
    f = open(dir + filename,'rb')
    return pickle.load(f)

# The high-level routines for dumping (loading) collections of flattened images to (from) a single file.

# This converts image arrays into flat lists before dumping to file.
def dump_cases(filename,digits=numpy.arange(10),type='training',dir=__mnist_path__,
               cases=None,labeled=True):
    images, labels = cases if cases else load_mnist(type, digits=digits)
    fcases = gen_flat_cases(cases=[images,labels])
    dump_flat_cases(filename,fcases,dir=dir,labeled=labeled)

# This loads any collection of flat MNIST cases from a file.
def load_cases(filename,dir=__mnist_path__,nested=True):
    fcases = load_flat_cases(filename,dir)
    return reconstruct_flat_cases(fcases,nested=nested)

# This is specialized to only load one of the two flat-case files:
# all_flat_mnist_training_cases or all_flat_mnist_testing_files
def load_all_flat_cases(type='training',dir=__mnist_path__):
    pair = load_flat_cases('all_flat_mnist_'+type+'_cases',dir=dir)
    return pair[0],pair[1]

def quicktest(n = 99):
    cases = load_all_flat_cases()
    features,labels = cases
    print(labels)
    image = reconstruct_image(features[n])
    show_digit_image(image)
    show_avg_digit(5)

