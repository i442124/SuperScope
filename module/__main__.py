import cv2
import numpy as np

from storage import games
from storage import images

from image_processing import camera
from image_processing import transform
from image_processing.feature import SIFT
from image_processing.feature import HIST
from image_processing.base64 import load_image


from scanner import draw_matches
from scanner import scan_for_matches

camera.capture()
while True:

    image = camera.get_current_frame()
    cv2.imshow('frame', image)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        
        query = transform.resize(image, height=256)
        best_match = scan_for_matches(query, images, top_n=1)
        
        target = load_image(best_match['image'])
        target = transform.resize(target, height=256)
        cv2.imshow('matches', draw_matches(query, target, best_match))

        if best_match['count'] > SIFT.MATCH_DESCRIPTOR_THRESHOLD:
            print(f"(Match count: {best_match['count']}) ({best_match['platform']}) - {best_match['title']}")
        else:
            print(f"(Match count: {best_match['count']}) No match found.")
        
        
