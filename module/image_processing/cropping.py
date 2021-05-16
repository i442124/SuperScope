import cv2
import numpy as np

# removes the black border from an
# image where the luminosity is below
# the specified threshold
def crop_boundaries(image, thresh=0):
    y_nonzero, x_nonzero, = np.nonzero(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) > thresh)
    return image[np.min(y_nonzero):np.max(y_nonzero), np.min(x_nonzero):np.max(x_nonzero)]
