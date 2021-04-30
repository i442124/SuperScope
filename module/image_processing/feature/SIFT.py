import cv2

N_KEYPOINTS = 500
MATCH_DESCRIPTOR_RATIO = 0.60
MATCH_DESCRIPTOR_THRESHOLD = 30

def extract_from_image(image):
    sift = cv2.SIFT_create(N_KEYPOINTS)
    return sift.detectAndCompute(image, mask=None)

def match_descriptors(query_desc, target_desc):
    matches = cv2.BFMatcher().knnMatch(query_desc, target_desc, 2)
    return [[m] for m, n in matches if m.distance < MATCH_DESCRIPTOR_RATIO * n.distance]

def get_match_count(desc_matches):
    return len({ m[0].trainIdx for m in desc_matches })
    