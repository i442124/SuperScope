import numpy as np
import pandas as pd

GAME_DETAILS_PATH = '../data/game_details.json'
GAME_REVIEWS_PATH = '../data/game_reviews.json'
GAME_IMAGES_PATH = '../data/box-art/small_set-256x-K500.pkl'

GAME_DETAILS_SELECTION = ['title', 'platform', 'publisher', 'genres']
GAME_REVIEWS_SELECTION = ['title', 'platform', 'meta_score', 'review_critic']
GAME_IMAGE_SELECTION = ['title', 'platform', 'image', 'histogram', 'keypoints', 'descriptors', 'structure']

games = pd.read_json(GAME_DETAILS_PATH)
games = games[GAME_DETAILS_SELECTION]

ratings = pd.read_json(GAME_REVIEWS_PATH)
ratings = ratings[GAME_REVIEWS_SELECTION]

images = pd.read_pickle(GAME_IMAGES_PATH)
images = pd.merge(games.reset_index(), images)
images = images[GAME_IMAGE_SELECTION]

ratings = ratings[ratings['review_critic'].notna()]
ratings = ratings[ratings['meta_score'].notna()]

games['genres'] = games['genres'].apply(lambda x: list(set(x)))
games = games.drop_duplicates(subset=['title', 'platform'])