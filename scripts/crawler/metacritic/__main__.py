import os
import json

from os import path
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spiders.list_spider import ListSpider
from spiders.reviews_spider import CriticReviewSpider


def list_all():
    settings = get_project_settings()
    settings['FEED_URI'] = 'games.json'
    settings['FEED_FORMAT'] = 'JSON'

    if os.path.exists(settings['FEED_URI']):
        os.remove(settings['FEED_URI'])

    process = CrawlerProcess(settings)
    process.crawl(ListSpider)
    process.start()

def critics(game_list):
    settings = get_project_settings()
    settings['FEED_URI'] = 'game_reviews.json'
    settings['FEED_FORMAT'] = 'JSON'
    settings['DOWNLOAD_DELAY'] = 2

    if os.path.exists(settings['FEED_URI']):
        os.remove(settings['FEED_URI'])

    process = CrawlerProcess(settings)
    process.crawl(CriticReviewSpider, game_list)
    process.start()


if __name__ == '__main__':

    list_all()
    with open ("games.json", "r") as myfile:
        critics([d['f'] for d in json.load(myfile)])