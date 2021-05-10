import keys
import helper
import argparse

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser(description='Image Feature Extractor')
parser.add_argument('file', help='File with list of MobyGames box-art images.')
parser.add_argument('-es', '--extract_structure', action='store_true', help='Extract the structural analysis image.')
parser.add_argument('-eh', '--extract_histogram', action='store_true', help='Extract the color histogram of the images.')
parser.add_argument('-ef', '--extract_features', action='store_true', help='Extract the keypoints and descriptors of images.')
parser.add_argument('-c', '--color', action='store_true', help='Retain color information in similarity image.')
parser.add_argument('-s', '--size', type=int, default=16, help='The size of the structual similarty image.')
parser.add_argument('-k', '--keypoints', type=int, default=500, help='The amount of keypoints to extract.')
parser.add_argument('-b', '--bins', type=int, default=8, help='The number of bins in the color histogram.')
parser.add_argument('-W', '--width', type=int, default=None, help='Width in pixels when extracting features.')
parser.add_argument('-H', '--height', type=int, default=None, help='Height in pixels when extracting features.')
parser.add_argument('-o', '--output', nargs='?', default='output', help='The name of the output file.')


def main():
    args = parser.parse_args()
    images = pd.read_json(args.file)

    if (args.extract_histogram):
        images['histogram'] = np.empty
    if (args.extract_structure):
        images['structure'] = np.empty
    if (args.extract_features):
        images['keypoints'] = np.empty
        images['descriptors'] = np.empty

    for idx, row in images.iterrows():
        print(f'Processing images: {idx+1} of {len(images)}', end='\r')
        image = helper.load_image(row['image'])
        image = helper.resize(image, width=args.width, height=args.height)

        if (args.extract_histogram):
            images.at[idx, 'histogram'] = helper.calcHist(image, args.bins)
        if (args.extract_structure):
            structure = image if args.color else helper.convert_to_black_white(image)
            images.at[idx, 'structure'] = helper.resize(structure, args.size, args.size)
        if (args.extract_features):
            key, desc = helper.extract_from_image(image, args.keypoints)
            images.at[idx, 'keypoints'], images.at[idx, 'descriptors'] = key, desc

    print('\nDone!')
    images.to_pickle(args.output)

if __name__ == '__main__':
    main()
