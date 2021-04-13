import tqdm
import scrapy

def extract_value(response, text_path):
    value = response.css(text_path).get()
    return None if not value else value.strip()

## ----------------------------CREATING THE SPIDER------------------------------

class CriticReviewSpider(scrapy.Spider):
    name = "critic-reviews"
    custom_settings = {
        'LOG_LEVEL' : 'ERROR',
        'RETRY_TIMES': 50 
    }
    
## ----------------------------DEFINING THE SPIDER------------------------------ 

    def __init__(self, game_list, **kwargs):
        self.start_urls = [f'https://www.metacritic.com{g}/critic-reviews' for g in game_list]
        self.pbar = tqdm.tqdm(total=len(game_list), desc="Scraping", unit="game", ascii=True)
        super().__init__(**kwargs)

## --------------------------GETTING CRITIC REVIEWS-----------------------------  

    def parse(self, response):

        ## The scraping of the reviews
        reviews_on_page = response.css('.critic_review .review_content')
        for review in reviews_on_page: yield {
            
            ## Title
            "title": extract_value(response, '.product_title h1 ::text'),
            ## Platform
            "platform": 
                extract_value(response, '.product_title .platform ::text') or 
                extract_value(response, '.product_title .platform a ::text'),

            ## Metascore
            "meta_score": extract_value(review, '.review_grade div ::text'),
            ## Critic Name
            "review_critic": extract_value(review, '.review_critic ::text'),
            ## Critic Reference
            "review_critic_page": extract_value(review, '.author_reviews a ::attr(href)'),

             # Review Date
             "review_data": extract_value(review, '.review_critic .date ::text'),
             # Review Source
             "review_source": extract_value(review, '.full_review a ::attr(href)'),
             # Review Content
             "review_content": extract_value(review, '.review_body ::text')
        }

## ----------------------------GOTO TO THE NEXT PAGE----------------------------

        # Update progress
        self.pbar.update(1)

        # Navigate to next page
        next_page = response.css('.next a ::attr(href)').get()
        if next_page: yield scrapy.Request(response.urljoin(next_page))

