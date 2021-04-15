import os
import sys
import json
import argparse

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spiders.list_spider import ListSpider
from spiders.litem_spider import ItemSpider
from spiders.reviews_spider import CriticReviewSpider

parser = argparse.ArgumentParser(description='Metacritic Scraper')
parser.add_argument('file', help='File with the list of pages to visit.')
parser.add_argument('action', choices=['details', 'reviews'], help='Type of content to scrape.')
parser.add_argument('-f', '--format', nargs='?', default='JSON', help='Format of the ouput file.')
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

    if args.action == 'details':
        game_list = load_file(args.file)
        delete_file_if_exists(args.output)
        process = CrawlerProcess(settings)
        process.crawl(ItemSpider, game_list)
        process.start()

    elif args.action == 'reviews':
        game_list = load_file(args.file)
        delete_file_if_exists(args.output)
        process = CrawlerProcess(settings)
        process.crawl(CriticReviewSpider, game_list)
        process.start()