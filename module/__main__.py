import cv2
import numpy as np
import pandas as pd

from storage import games
from storage import images
from storage import ratings

from image_processing import camera
from image_processing.base64 import load_image
from image_processing.metascore import game_not_found
from image_processing.metascore import game_not_rated
from image_processing.metascore import create_meta_score

from scanner import draw_matches
from scanner import scan_for_matches
from scanner import MATCH_DESCRIPTOR_THRESHOLD

from recommender import find_clusters
from recommender import get_recommendation_scores

my_ratings = pd.read_csv('../data/user-reviews/my-game-ratings.csv')
my_ratings['review_critic'] = 'self'

ratings = find_clusters(ratings.append(my_ratings))
cluster = ratings[ratings['review_critic'] == 'self']['cluster'].iloc[0]
s = get_recommendation_scores(ratings, cluster=cluster, penalizer_strength=0.5)

camera.capture()
while True:

    image = camera.get_current_frame()
    cv2.imshow('frame', image)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        
        best_match = scan_for_matches(image, top_n=1)
        best_match_image = load_image(best_match['image'])
        cv2.imshow('matches', draw_matches(image, best_match_image, best_match))

        if best_match['count'] > MATCH_DESCRIPTOR_THRESHOLD:
            print(f"(Match count: {best_match['count']}) ({best_match['platform']}) - {best_match['title']}")
            best_match_scores = s.loc[(s['title'] == best_match['title']) & (s['platform'] == best_match['platform'])]['recommendation_score']
            cv2.imshow('score', create_meta_score(best_match_scores.iloc[0]) if len(best_match_scores) else game_not_rated())
        else:
            print(f"(Match count: {best_match['count']}) No match found.")
            cv2.imshow('score', game_not_found())
