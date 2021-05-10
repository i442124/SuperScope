import cv2
from skimage import data, img_as_float
from skimage.metrics import normalized_root_mse
from skimage.metrics import structural_similarity

def preprocess_image(image):
    return cv2.resize(image, (16,16))

def compare_ssim(query_image, target_image):
    return structural_similarity(query_image, target_image, multichannel=True)

def compare_nrmse(query_image, target_image):
    return normalized_root_mse(query_image, target_image, normalization='min-max')