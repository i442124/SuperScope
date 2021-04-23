import tqdm
import scrapy
import requests

from .helpers import *
from base64 import b64encode

class ImageSpider(scrapy.Spider):
    name="image-spider"
    custom_settings =  {
        'LOG_LEVEL': 'ERROR',
        'RETRY_TIMES': 50
    }


    def __init__(self, game_list):
        self.start_urls = parse_url(game_list, '/cover-art')
        self.pbar = pbar(count=len(game_list))
        
    def start_requests(self):
        for index, url in enumerate(self.start_urls):
            yield scrapy.Request(url, callback=self.parse, meta={'index': index })

    def parse(self, response):
        # try:
        for image_url in extract_image_urls(response):
            image = b64encode(requests.get(image_url).content)
            yield { 'index': response.meta['index'], 'image': image.decode('utf-8') }
        # finally:
        self.pbar.update(1)