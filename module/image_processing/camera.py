import cv2

# global variable for
# the current camera
feed = None

# captures the camera
# and sets it as the current
def capture(cid=0):
    global feed
    feed = cv2.VideoCapture(cid)

# captures the current frame
# of the current camera
def get_current_frame():
    s, image = feed.read()
    return image

# releases the current camera
# and frees it
def release():
    feed.release()
