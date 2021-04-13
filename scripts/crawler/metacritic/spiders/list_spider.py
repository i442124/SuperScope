import tqdm
import scrapy

## ----------------------------CREATING THE SPIDER------------------------------

class ListSpider(scrapy.Spider):
    name = "list"
    custom_settings = {
        'LOG_LEVEL' : 'ERROR'
    }

## ----------------------------DEFINING THE SPIDER------------------------------ 

    def __init__(self, start_page=0, **kwargs):
        self.start_urls = [f'https://www.metacritic.com/browse/games/score/metascore/all/all/filtered?page={start_page}']
        self.start_page = int(start_page)
        super().__init__(**kwargs)

## ----------------------------GETTING GAMES URLs-------------------------------  

    def parse(self, response):

        # Get the current page we are visiting
        # because we only need to summon the loading bar on the first page
        current_page = int(response.css('.active_page span ::text').get()) - 1
        if current_page == self.start_page:

            ## Create the loading bar!
            last_page_num = int(response.css('.last_page a ::text').get())        
            self.pbar = tqdm.tqdm(total=last_page_num - self.start_page, desc="Listing games", unit='page', ascii=True)

        ## The scraping of the items
        items_on_page = response.css('.browse_list_wrapper a.title::attr(href)').getall()
        for item in items_on_page: yield { 'f': item }

## ----------------------------GOTO TO THE NEXT PAGE----------------------------
        
        # Update progress
        self.pbar.update(1)

        # Navigate to next page
        next_page = response.css('.next a ::attr(href)').get()
        if next_page: yield scrapy.Request(response.urljoin(next_page))
