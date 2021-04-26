import cv2

N_KEYPOINTS = 500
MATCH_DESCRIPTOR_RATIO = 0.75
MATCH_DESCRIPTOR_THRESHOLD = 80

def extract_from_image(image):
    sift = cv2.SIFT_create(N_KEYPOINTS)
    return sift.detectAndCompute(image, mask=None)

def match_descriptors(query_desc, target_desc):
    matches = cv2.BFMatcher().knnMatch(query_desc, target_desc, 2)
    return [[m] for m, n in matches if m.distance < MATCH_DESCRIPTOR_RATIO * n.distance]