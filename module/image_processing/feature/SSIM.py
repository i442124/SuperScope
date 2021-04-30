import cv2
from skimage import data, img_as_float
from skimage.metrics import structural_similarity

def preprocess_image(image):
    return cv2.resize(image, (16,16))

def compare(query_image, target_image):
    return structural_similarity(query_image, target_image, multichannel=True)