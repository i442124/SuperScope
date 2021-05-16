import cv2

# Resizes an image while maintaining aspect
# ratio if one of the axis is not provided
def resize_maintain_aspect(image, height=None, width=None):

    # extract the dimensions target
    # and actual dimensions of the image
    dim = (width, height)
    h, w = image.shape[:2]

    # calculate the width
    # if not provided
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    
    # calculate the height
    # if not provided
    elif height is None:
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image with the
    # auto calculated dimensions
    return cv2.resize(image, dim)
