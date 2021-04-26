import cv2


def resize(image, width=None, height=None):

    dim = (height, width)
    h, w = image.shape[:2] 

    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)   
    
    elif height is None:
        r = width / float(w)
        dim = (width, int(h * r))
        
    return cv2.resize(image, dim)