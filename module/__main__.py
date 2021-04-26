import cv2
import numpy as np

from storage import games
from storage import images

from image_processing import base64
from image_processing import camera
from image_processing.feature import SIFT

from scanner import scan_for_matches

camera.capture()
while(True):

    image = camera.get_current_frame()
    cv2.imshow('frame', image)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        best_match = scan_for_matches(image, images)
        if len(best_match['matches']) > SIFT.MATCH_DESCRIPTOR_THRESHOLD:
            cv2.imshow('result', base64.load_image(best_match['image']))
            print(f"(Match count: {len(best_match['matches'])}) ({best_match['platform']}) - {best_match['title']}")
        else:
            cv2.imshow('result', np.zeros((512, 512, 3), np.uint8))
            print(f"(Match count: {len(best_match['matches'])}) No match found.")
