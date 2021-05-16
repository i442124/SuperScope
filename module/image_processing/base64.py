import cv2
import base64
import numpy as np

# Read a base64 encoded files
# and returns it as an image
def read_image(path):
    text = open(path).read()
    return load_image(data=text)

# Loads a base64 encoded string
# and return it as an image
def load_image(data):
    img = base64.b64decode(data)
    array = np.fromstring(img, dtype=np.uint8)
    return cv2.imdecode(array, cv2.IMREAD_COLOR)
