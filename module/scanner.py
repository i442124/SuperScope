import cv2
from image_processing import base64
from image_processing.feature import HIST
from image_processing.feature import SIFT
from image_processing.feature import SSIM
from image_processing.transform import resize

def best_histogram_matches(image, targets):
    correlations = []
    hist = HIST.get(image)
    for target in targets:
        corr = HIST.compare(hist, target['histogram'])
        correlations.append(corr)

    matcher = lambda pair: pair[0]
    matches = zip(correlations, targets)
    matches = [x for _, x in sorted(matches, key=matcher, reverse=True)]
    return matches[:3500]


def best_ssim_matches(image, targets):
    similarities = []
    image = SSIM.prepare(image)

    for target in targets:
        ssim = SSIM.compare(image, target['structure'])
        similarities.append(ssim)

    matcher = lambda pair: pair[0]
    matches = zip(similarities, targets)
    matches = [x for _, x in sorted(matches, key=matcher, reverse=True)]
    return matches[:800]

def best_sift_match(image, targets):

    matches = []
    key, desc = SIFT.extract_from_image(image)
    for target in targets:
        desc_matches = SIFT.match_descriptors(desc, target['descriptors'])
        matches.append({ 'title': target['title'], 'platform': target['platform'], 'image':target['image'], 'keypoints': target['keypoints'], 'matches':desc_matches })
    
    best_match = sorted(matches, key=lambda x: len(x['matches']), reverse=True)[0]
    cv2.imshow('match', cv2.drawMatchesKnn(image, key, resize(base64.load_image(best_match['image']), height=256), best_match['keypoints'], best_match['matches'], None, flags=2))
    return best_match

def scan_for_matches(query_image, targets):
    image = resize(query_image, height=256)
    targets = targets.to_dict(orient='records')

    ## COMPARE WITH HISTOGRAMS THAT ARE CLOSEST
    targets = best_histogram_matches(image, targets)

    ## COMPARE WITH BEST SIMLIARITIES BETWEEN IMAGES (SSIM)
    targets = best_ssim_matches(image, targets)

    ## COMPARE WITH BEST SIMILARITIES BETWEEN IMAGES (SIFT)
    target = best_sift_match(image, targets)
    return target