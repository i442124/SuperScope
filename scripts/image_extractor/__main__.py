import keys
import helper
import argparse

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser(description='Image Feature Extractor')
parser.add_argument('file', help='File with list of MobyGames box-art images.')
parser.add_argument('-W', '--width', type=int, default=None, help='The width of the images.')
parser.add_argument('-H', '--height', type=int, default=None, help='The height of the images.')
parser.add_argument('-k', '--keypoints', type=int, default=None, help='Export keypoints and descriptors.')
parser.add_argument('-hs', '--histogram', action='store_true', help='Export the color histogram of the images.')
parser.add_argument('-s', '--structure', action='store_true', help='Export the structure of the image.')
parser.add_argument('-o', '--output', nargs='?', default='output', help='Name of the output file.')

if __name__ == '__main__':

    args = parser.parse_args()
    images = pd.read_json(args.file)[:1]
    
    if (args.histogram):
        images['histogram'] = np.empty
    if (args.keypoints):
        images['keypoints'] = np.empty
        images['descriptors'] = np.empty
    if (args.structure):
        images['structure'] = np.empty

    for idx, row in images.iterrows():
        print(f'{idx} of {len(images)}')
        image = helper.load_image(row['image'])
        image = helper.resize(image, width=args.width, height=args.height)
        
        if (args.histogram):
            images.at[idx, 'histogram'] = helper.calcHist(image)
        if(args.keypoints):
            key, desc = helper.extract_from_image(image, args.keypoints)
            images.at[idx, 'keypoints'], images.at[idx, 'descriptors'] = key, desc
        if(args.structure):
            images.at[idx, 'structure'] = helper.resize(image, 16, 16)

    print(images['structure'])  
    images.to_pickle(args.output)
