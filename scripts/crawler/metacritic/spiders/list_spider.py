import tqdm
import scrapy
from .helpers import *

## ----------------------------CREATING THE SPIDER------------------------------

class ListSpider(scrapy.Spider):
    name = "list"
    custom_settings = {
        'LOG_LEVEL':'ERROR',
        'RETRY_TIMES': 50
    }

## ----------------------------DEFINING THE SPIDER------------------------------ 

    def __init__(self, start_page=0):
        self.start_urls = [f'{METACRITIC_LIST_ALL}?page={start_page}']
        self.start_page = int(start_page)

## ----------------------------GETTING GAMES URLs-------------------------------

    def parse(self, response):

        # Get the current page we are visiting
        # because we only need to summon the loading bar on the first page
        current_page = int(response.css('.active_page span ::text').get()) - 1
        if current_page == self.start_page:

            ## Create the loading bar!
            page_count = self.settings['CLOSESPIDER_PAGECOUNT']
            last_page_num = int(response.css('.last_page a ::text').get())
            
            page_count = last_page_num if page_count == 0 else page_count 
            self.pbar = tqdm.tqdm(total=page_count - self.start_page, desc="Listing games", unit='page', ascii=True)

        ## The scraping of the items
        items_on_page = response.css('.browse_list_wrapper a.title::attr(href)').getall()
        for item in items_on_page: yield { 'f': item }

## ----------------------------GOTO TO THE NEXT PAGE----------------------------
        
        # Update progress
        self.pbar.update(1)

        # Navigate to next page
        next_page = response.css('.next a ::attr(href)').get()
        if next_page: yield scrapy.Request(response.urljoin(next_page))
