import cv2
import base64
import numpy as np

def load_image(data):
    img = base64.b64decode(data)
    array = np.fromstring(img, dtype=np.uint8)
    return cv2.imdecode(array, cv2.IMREAD_COLOR)