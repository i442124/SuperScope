import cv2

def get(image):
    hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0,256,0,256,0,256])
    hist = cv2.normalize(hist, None)
    return hist

def compare(histA, histB):
    return cv2.compareHist(histA, histB, cv2.HISTCMP_CORREL)