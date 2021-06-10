from flask import Flask
from flask import request
from flask_cors import CORS

import numpy as np
import pandas as pd
from io import BytesIO

from storage import games
from storage import ratings

from scanner import draw_matches
from scanner import scan_for_matches

from recommender import find_clusters
from recommender import get_recommendation_scores

from image_processing.base64 import load_image

app = Flask(__name__)
app.config["DEBUG"] = False

CORS(app)

@app.route('/api/v1/scanner/', methods=['POST'])
def api_scan_for_matches():

    # take the top_n results or 
    # fallback to the default value
    top_n = dict(default=1, type=int)
    top_n = request.args.get('top_n', **top_n)

    use_ssim = dict(default='false', type=str)
    use_ssim = request.args.get('use_ssim', **use_ssim) == 'true'

    use_hist = dict(default='false', type=str)
    use_hist = request.args.get('use_hist', **use_hist) == 'true'

    # load the image that was send by the 
    # user and scan for the best matches
    # that we can find in the dataset
    image = load_image(request.data)
    best_match = scan_for_matches(image, top_n=top_n, use_hist=use_hist, use_ssim=use_ssim)

    # return the top_n results back to the user,
    # the format depends on if the users requested
    # a singluar best match, or the set of best matches
    orient = 'records' if top_n > 1 else 'columns'
    return best_match[['title', 'platform', 'image', 'count']].to_json(orient=orient)

@app.route('/', methods=['GET'])
def api_ok():
    return "Ok"

@app.route('/api/v1/recommendations/', methods=['POST'])
def api_get_recommendation_scores():

    # convert the ratings of the 
    # user into a pandas dataframe 
    user_ratings = pd.read_csv(BytesIO(request.data))
    user_ratings['review_critic'] = 'USER'

    # Look for clusters in the dataset and join the
    # user that send the request into one of them
    cluster_ratings = find_clusters(ratings.append(user_ratings))
    cluster = cluster_ratings[cluster_ratings['review_critic'] == 'USER']['cluster'].iloc[0]
    
    # return the recommendation scores of the cluster that the user belongs
    s = get_recommendation_scores(cluster_ratings, cluster=cluster, penalizer_strength=0.5)
    return s.to_json(orient='records')

ssl_context = ('certificates/cert.pem', 'certificates/pkey.pem')
app.run(host='0.0.0.0', ssl_context=ssl_context)