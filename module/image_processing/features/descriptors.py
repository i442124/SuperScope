import cv2

# Number of keypoints (features)
# to extract from an image
N_KEYPOINTS = 500

# The distance ratio between the two
# nearest matches of keypoints
MATCH_DESCRIPTOR_RATIO = 0.60

# The matcher to use when comparing
# two discriptors with each other
DESCRIPTOR_MATCHER = cv2.DescriptorMatcher_BRUTEFORCE

# Extracts the SIFT features
# from an image and returns
def extract_from_image(image):
    sift = cv2.SIFT_create(N_KEYPOINTS)
    return sift.detectAndCompute(image, mask=None)

# Matches the descriptors of two
# images and returns the all good
# matches according to Lowe's ratio test
def match(descA, descB, matcher=DESCRIPTOR_MATCHER):
    matches = cv2.DescriptorMatcher_create(matcher).knnMatch(descA, descB, 2)
    return [[m] for m, n in matches if m.distance < MATCH_DESCRIPTOR_RATIO * n.distance]

# Returns the unique number of
# matched keypoints between two images
def get_unique_count(desc_matches):
    return len({ m[0].trainIdx for m in desc_matches})
