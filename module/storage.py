import ast
import numpy as np
import pandas as pd


GAME_DETAILS_PATH = '../data/video-games/game-details.csv'
GAME_REVIEWS_PATH = '../data/video-games/game-reviews.csv'
GAME_IMAGES_PATH = '../data/box-art/small_set-256x-K500.pkl'

GAME_IMAGE_SELECTION = ['title', 'platform', 'image', 'histogram', 'keypoints', 'descriptors', 'structure']

games = pd.read_csv(GAME_DETAILS_PATH)
ratings = pd.read_csv(GAME_REVIEWS_PATH)

images = pd.read_pickle(GAME_IMAGES_PATH)
images = pd.merge(games.reset_index(), images)
images = images[GAME_IMAGE_SELECTION]