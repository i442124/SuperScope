import tqdm
import scrapy
import requests

from .helpers import *
from base64 import b64encode

## ----------------------------CREATING THE SPIDER------------------------------

class ItemSpider(scrapy.Spider):
    name="list-item"
    custom_settings = {
        'LOG_LEVEL':'ERROR',
        'RETRY_TIMES': 50
    }

## ----------------------------DEFINING THE SPIDER------------------------------ 

    def __init__(self, game_list):
        self.start_urls = parse_url(game_list)
        self.pbar = pbar(count=len(game_list))

## ----------------------------GETTING GAMES URLs-------------------------------

    def parse(self, response):

        thumbnail = extract_value(response, '.product_data .product_image ::attr(src)')
        thumbnail = b64encode(requests.get(thumbnail).content)
        
        yield {     
            ## Title
            "title": extract_value(response, '.product_title h1 ::text'),
            ## Platform
            "platform": 
                extract_value(response, '.product_title .platform ::text') or 
                extract_value(response, '.product_title .platform a ::text'),

            # Publisher
            "publisher": extract_value(response, '.product_data .publisher .data a::text'),
            "publisher_page": extract_value(response, '.product_data .publisher .data a ::attr(href)'),

            # Developer
            "developer": extract_value(response, '.product_data .developer .data a ::text'),
            "developer_page": extract_value(response, '.product_data .developer .data a ::attr(href)'),

            # Release Date
            "release_date": extract_value(response, '.product_data .release_data .data ::text'),

            # Genre(s)
            "genres": extract_values(response, '.product_data .product_genre .data ::text'),
            
            # Summary
            "summary": extract_value(response, '.product_data .product_summary .data .blurb_expanded ::text'),

            # Artwork of Box
            "thumbnail": thumbnail.decode('utf-8')
        }

## ----------------------------GOTO TO THE NEXT PAGE----------------------------
        
        # Update progress
        self.pbar.update(1)

        # Navigate to next page
        next_page = response.css('.next a ::attr(href)').get()
        if next_page: yield scrapy.Request(response.urljoin(next_page))