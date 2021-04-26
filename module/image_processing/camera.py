import cv2

feed = None

def capture(cid=0):
    global feed 
    feed = cv2.VideoCapture(cid)

def get_current_frame():
    s, image = feed.read()
    return image

def release():
    feed.release()
    