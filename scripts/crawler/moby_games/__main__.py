import os
import sys
import json
import argparse

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spiders.image_spider import ImageSpider

parser = argparse.ArgumentParser(description='MobyGames Scraper')
parser.add_argument('file', help='File with the list of pages to visit.')
parser.add_argument('-f', '--format', nargs='?', default='JSON', help='Format of the output file.')
parser.add_argument('-o', '--output', nargs='?', default='output', help='Name of the output file.')

def load_file(path):
    with open(path, 'r') as filename:
        return [d['f'] for d in json.load(filename)]

def delete_file_if_exists(path):
    if os.path.isfile(path):
        os.remove(path)

if __name__ == '__main__':

    args = parser.parse_args()
    settings = get_project_settings()
    settings['FEED_URI'] = args.output
    settings['FEED_FORMAT'] = args.format
    settings['DOWNLOAD_DELAY'] = 10

    game_list = load_file(args.file)
    delete_file_if_exists(args.output)

    process = CrawlerProcess(settings)
    process.crawl(ImageSpider, game_list)
    process.start()