import ast
import numpy as np
import pandas as pd

GAME_DETAILS_PATH = '../data/video-games/game-details.csv'
GAME_REVIEWS_PATH = '../data/video-games/game-reviews.csv'
GAME_IMAGES_PATH = '../data/box-art/small_set-256x-K500.pkl'

## Load game details from path
## Don't forget to convert string back to list
games = pd.read_csv(GAME_DETAILS_PATH)
games['genres'] = games['genres'].apply(ast.literal_eval)

## Load the ratings of all games
ratings = pd.read_csv(GAME_REVIEWS_PATH)

## Load the box-art images of all games
images = pd.read_pickle(GAME_IMAGES_PATH)