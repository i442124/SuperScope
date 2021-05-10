import cv2

feed = None

def capture(cid=0):
    global feed 
    feed = cv2.VideoCapture(cid)

def get_current_frame():
    s, image = feed.read()
    image = crop_black_pixels(image)
    return image

def crop_black_pixels(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x,y,w,h = cv2.boundingRect(cnt)
    crop = image[y:y+h,x:x+w]
    return crop

def release():
    feed.release()
    