import os
import os.path

import cv2
import base64
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import numpy as np
import pandas as pd
import seaborn as sns

# This method lists all files
# that can be found in a directory
def list_files(path):
    fnames = os.listdir(path)
    abspath = lambda x: os.path.join(path, x)
    return [abspath(file) for file in fnames]


# This method loads an
# image from a specified path
def load_image(path):
    image = cv2.imread(path)
    BGR2RGB = cv2.COLOR_BGR2RGB
    return cv2.cvtColor(image, BGR2RGB)


# This method loads an
# image from a base64 string
def load_image_from_string(base64_image):
    BGR2RGB = cv2.COLOR_BGR2RGB
    decoded = base64.b64decode(base64_image)
    array = np.fromstring(decoded, dtype=np.uint8)
    return cv2.cvtColor(cv2.imdecode(array, cv2.IMREAD_COLOR), BGR2RGB)

# This methods loads all images
# in a directory in a directory
def load_images_in_dir(path):
    fnames = list_files(path)
    images = [load_image(f) for f in fnames]
    labels = [os.path.basename(f) for f in fnames]
    return pd.DataFrame({ 'label': labels, 'image': images })

# This methods returns a
# new instance of the image resized
def resize_image(image, height=None, width=None):
    if height is not None or width is not None:
        dim = (width, height)
        h, w = image.shape[:2] 
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)      
        elif height is None:
            r = width / float(w)
            dim = (width, int(h * r))  
        image = cv2.resize(image, dim)
    return image

# Plots the set of images from
# a column in the provided dataset
def spectate_image_set(images, column='image'):
    plt.figure(figsize=(3.6 * len(images), 4.8))
    for idx, (image) in images.iterrows():
        plt.subplot(1, len(images), idx+1)
        plt.xlabel(image['label'])
        plt.imshow(image[column])


# Sorts values from a matrix on a per row basis,
# in either ascending or decending order with
# color coded with the Y-values
def plot_correlation_matrix(matrix, ascending=True, cmap=plt.cm.viridis, legend=True, annot=True, annot_label='{:.2f}'):

    points = []
    nrows = len(matrix.index)
    ncols = len(matrix.columns)
    
    for y, y_label in enumerate(matrix.index):

        values = matrix.iloc[y]
        values = values.sort_values(ascending=ascending)
        for x, x_label in enumerate(matrix.columns):
            idx = matrix.columns.get_loc(values.index[x])
            points.append(matrix.columns.get_loc(values.index[x]))
            if annot: plt.text(x, y, annot_label.format(values[x]), ha='center', va='center', color='w' if idx < ncols / 2 else 'k')
                
    plt.xticks([])
    plt.yticks(range(nrows), matrix.index)
    plt.imshow(np.reshape(points, (nrows, ncols)), cmap=cmap)
    if legend: plt.legend([mpatches.Patch(color=cmap(idx / (nrows - 1))) for idx in range(nrows)], matrix.index, bbox_to_anchor=(1, 1), loc="upper left")