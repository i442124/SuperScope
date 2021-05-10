import cv2
import numpy as np
import pandas as pd

from image_processing import base64
from image_processing import transform
from image_processing.feature import HIST
from image_processing.feature import SSIM
from image_processing.feature import SIFT

def draw_matches(query, target, match):
    image_features = (query, match['q_keypoints'], target, match['t_keypoints'])
    return cv2.drawMatchesKnn(*image_features, match['matches'], None, flags=2)

def best_histogram_matches(histogram, targets):
    matches = pd.DataFrame(targets[['title', 'platform', 'histogram']])
    matches['correlation'] = matches['histogram'].apply(lambda x: HIST.compare(histogram, x))
    return matches.sort_values(by='correlation', ascending=False)

def best_ssim_matches(structure, targets):
    matches = pd.DataFrame(targets[['structure', 'platform', 'title']])
    matches['similarity'] = matches['structure'].apply(lambda x: SSIM.compare_nrmse(structure, x))
    return matches.sort_values(by='similarity', ascending=True)

def get_descriptor_matches(desc, targets):
    desc_matches = targets['descriptors'].apply(lambda x: SIFT.match_descriptors(desc, x))
    match_count = desc_matches.apply(lambda x: SIFT.get_match_count(x))
    return desc_matches, match_count


def scan_for_matches(query, targets, top_n=1):

    ## USE COLOR HISTOGRAMS TO FILTER OUT IMAGES 
    ## WITH COLORS THAT DIFFER TO MUCH FROM QUERY COLORS
    # histogram = HIST.extract_from_image(query)
    # histogram_matches = best_histogram_matches(histogram, targets)
    # targets = targets.reindex(histogram_matches.index, copy=True).iloc[:800]

    ## USE SIMILARITY INDEX TO FILTER OUT IMAGES 
    ## THAT DIFFER TOO MUCH FROM QUERY STRUCTURE

    ssim = SSIM.preprocess_image(query)
    ssim_matches = best_ssim_matches(ssim, targets)
    targets = targets.reindex(ssim_matches.index, copy=True).iloc[:800]

    ## USE THE SIFT KEYPOINTS AND DESCRIPTORS TO
    ## LOOK FOR THE STRONGEST CORRELATION BETWEEN IMAGES
    q_keys, q_desc = SIFT.extract_from_image(query)
    t_keys, t_desc = targets['keypoints'], targets['descriptors']
    desc_matches, match_count = get_descriptor_matches(q_desc, targets)

    ## CREATE NICE STRUCTURE FOR THE MATCHES SO
    ## WE CAN EASILY DRAW THE KEYPOINTS IF WE NEED TO
    matches = pd.DataFrame(targets[['title', 'platform', 'image']])
    matches['q_keypoints'] = [q_keys] * len(matches)
    matches['t_keypoints'] = t_keys
    matches['matches'] = desc_matches
    matches['count'] = match_count

    ## SORT VALUES BY THE NUMBER OF FEATURES MATCHED
    ## TOP RESTULT IS MOST LIKELY THE IMAGE WE ARE LOOKING FOR
    matches.sort_values(by='count', ascending=False, inplace=True)
    return matches.iloc[:top_n] if top_n > 1 else matches.iloc[top_n]
