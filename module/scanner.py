import cv2
import time
import numpy as np
import pandas as pd

from storage import games
from storage import images

from image_processing import base64
from image_processing import cropping
from image_processing import transform
from image_processing.features import color_histogram
from image_processing.features import descriptors
from image_processing.features import structure

## IN THE NOTEBOOK FOR COLOR HISTOGRAMS
## WE CONCLUDED THAT THERE IS NO GOOD
## CORRELATION IN THE HISTOGRAMS
USE_COLOR_HISTOGRAM_TO_FILTER = False

## IN THE NOTEBOOK FOR IMAGE SIMILARITY
## WE CONCLUDED THAT IT WOULD BE A MAJOR BENIFIT
## TO FILTER THE SELECTION OF IMAGES TO ONLY THE TOP RESULTS
USE_IMAGE_SIMILARITY_TO_FILTER = False

## THE MINIMUM NUMBER OF MATCHES
## TO BE CONSIDERED THE SAME IMAGE
MATCH_DESCRIPTOR_THRESHOLD = 30

def ensure_image_dimensions(image):
    ## CROP THE BLACK BORDERS FROM THE CAMERA
    image = cropping.crop_boundaries(image)
    
    ## AND TRANSFORM THE IMAGE TO THE RESOLUTION CONFIGURED IN 
    ## THE DATA STORAGE SOLUTION, (MUST BE SAME VALUE AS PREPROCESS_IMAGE_SIZE)
    return transform.resize_maintain_aspect(image, height=256)

# SORTS THE IMAGES BASED ON THE CORRELATION
# BETWEEN THE QUERY HISTOGRAM AND TARGET HISTOGRAMS
def best_histogram_matches(hist, images):
    matches = images.histogram.apply(color_histogram.compare_corr, args=[hist])
    return matches.sort_values(ascending=False)

# SORTS THE IMAGES BASED ON THE SIMILARITY SCORES
# BETWEEN THE QUERY STRUCUTER AND TARGET STRUCUTRES
def best_structure_matches(struct, images):
    matches = images.structure.apply(structure.compare_nrmse, args=[struct])
    return matches.sort_values(ascending=True)

def best_descriptor_matches(desc, images):
    matches = images.descriptors.apply(descriptors.match, args=[desc])
    return matches, matches.apply(descriptors.get_unique_count)

def scan_for_matches(image, top_n=1, use_hist=USE_COLOR_HISTOGRAM_TO_FILTER, use_ssim=USE_IMAGE_SIMILARITY_TO_FILTER):

    ## INITIALIZE FULL SET OF TARGET IMAGES
    filtered_images = images

    ## ENSURE THAT THE QUERY IMAGE IS PROPERLY
    ## SCALED BEFORE PERFORMING ANY OPERATIONS
    image = ensure_image_dimensions(image)

    ## USE COLOR HISTGORAM TO FILTER OUT IMAGES
    ## WITH COLORS THAT DIFFER TO MUCH FROM THE QUERY IMAGE
    if use_hist:
        hist = color_histogram.extract_from_image(image)
        hist_matches = best_histogram_matches(hist, filtered_images)
        filtered_images = filtered_images.reindex(hist_matches.index).loc[:3500]

    ## USE SIMILARITY INDEX TO FILTER OUT IMAGES
    ## THAT DIFFER TOO MUCH FROM QUERY STRUCTURE
    if use_ssim:
        struct = structure.extract_from_image(image)
        struct_matches = best_structure_matches(struct, filtered_images)
        filtered_images = filtered_images.loc[struct_matches.index[:1200]]

    ## USE THE SIFT KEYPOINTS AND DESCRIPTORS TO
    ## LOOK FOR THE NUMBER OF MATCHES BETWEEN IMAGES
    q_keys, q_desc = descriptors.extract_from_image(image)
    t_keys, t_desc = filtered_images.keypoints, filtered_images.descriptors
    desc_matches, match_count = best_descriptor_matches(q_desc, filtered_images)

    ## CREATE A NEW DATAFRAME WITH ALL THE MATCH RESULTS
    matches = pd.DataFrame(filtered_images[['title', 'platform', 'image']])
    matches['q_keypoints'] = [q_keys] * len(matches)
    matches['t_keypoints'] = t_keys
    matches['matches'] = desc_matches
    matches['count'] = match_count

    ## AND SORT THEM BY THE NUMBER OF DESCRIPTORS MATCHED
    ## THE TOP RESULTS IS MOST LIKELY THE VIDEO GAME
    ## THAT WAS BEING SCANNED BY THE USERS (IF IT
    ## EXISTS IN THE DATASET OF COURSE)
    matches.sort_values(by='count', ascending=False, inplace=True)
    return matches.iloc[:top_n] if top_n > 1 else matches.iloc[top_n]


## DRAWS THE MATCHED KEYPOINTS BETWEEN A 
## QUERY AND TARGET IMAGE ON A NEW IMAGE
def draw_matches(query, target, match):
    query = ensure_image_dimensions(query)
    target = ensure_image_dimensions(target)
    image_features = (target, match['t_keypoints'], query, match['q_keypoints'])
    return cv2.drawMatchesKnn(*image_features, match['matches'], None, flags=2)
