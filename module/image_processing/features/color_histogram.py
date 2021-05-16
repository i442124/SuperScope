import cv2

## color values are stored in byte values between 0 - 255
## bins group the entire range of values into
## the total number of bins available.
N_BINS = 8

# whether to normalize the number of
# pixels to a ratio between 0 and 1.
NORMALIZE = True

# extract the color histogram of an image
# with the provided number of bins, normalize and return
def extract_from_image(image, n_bins=N_BINS, normalize=NORMALIZE):
    hist = cv2.calcHist([image], [0, 1, 2], None, [n_bins, n_bins, n_bins], [0, 256, 0, 256, 0, 256])
    hist = cv2.normalize(hist, None) if NORMALIZE else hist
    return hist

# extract the color histogram of an image in a path
# with the provided number of bins, normalize and return
def extract_from_path(path, n_bins=N_BINS, normalize=NORMALIZE):
    return extract_from_image(cv2.imread(path), n_bins, normalize)

# compares the histogram using
# the correlation between them
def compare_corr(histA, histB):
    CORREL = cv2.HISTCMP_CORREL
    return cv2.compareHist(histA, histB, CORREL)

## compares the histogram using
# the intersection between them
def compare_intrsct(histA, histB):
    INTRSCT = cv2.HISTCMP_INTERSECT
    return cv2.compareHist(histA, histB, INTRSCT)
