import cv2
import base64
import numpy as np

def load_image(base64_image):
    img = base64.b64decode(base64_image)
    array = np.fromstring(img, dtype=np.uint8)
    return cv2.imdecode(array, cv2.IMREAD_COLOR)

def convert_to_black_white(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def resize(image, height=None, width=None):
    if height is not None or width is not None:
        dim = (height, width)
        h, w = image.shape[:2] 
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)      
        elif height is None:
            r = width / float(w)
            dim = (width, int(h * r))  
        image = cv2.resize(image, dim)
    return image

def calcHist(image):
    ranges = [[0, 1, 2], [8, 8, 8], [0, 256,0,256,0,256]]
    histogram = cv2.calcHist([image], ranges[0], None, ranges[1], ranges[2])
    histogram = cv2.normalize(histogram, None)
    return histogram

def extract_from_image(image, N_KEYPOINTS=500):
    SIFT = cv2.SIFT_create(N_KEYPOINTS)
    return SIFT.detectAndCompute(image, mask=None)