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
parser.add_argument('-s', '--start_page', type=int, default=0, help="Page number to begin scraping.")
parser.add_argument('-c', '--page_count', type=int, default=0, help="Total number of pages to scrape.")
parser.add_argument('-f', '--format', nargs='?', default='JSON', help='Format of the ouput file.')
parser.add_argument('-o', '--output', nargs='?', default='output', help='Name of the output file.')

if __name__ == '__main__':

    args = parser.parse_args()
    settings = get_project_settings()
    settings['FEED_URI'] = args.output
    settings['FEED_FORMAT'] = args.format
    settings['CLOSESPIDER_PAGECOUNT'] = args.page_count

    if os.path.isfile(args.output):
        os.remove(args.output)

    process = CrawlerProcess(settings)
    process.crawl(ListSpider, args.start_page)
    process.start()