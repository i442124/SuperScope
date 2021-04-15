import tqdm
import scrapy

METACRITIC_BASE = "https://www.metacritic.com"
METACRITIC_LIST_ALL = "https://www.metacritic.com/browse/games/score/metascore/all"

def pbar(count):
    params = dict(desc='Scraping', unit='game', ascii=True)
    return tqdm.tqdm(total=count, **params)

def parse_url(game_list, subdir=''):
    expression = lambda x: METACRITIC_BASE + x
    return [expression(d + subdir) for d in game_list]

def extract_value(response, text_path):
    value = response.css(text_path).get()
    return None if not value else value.strip()

def extract_values(response, text_path):
    values = response.css(text_path).getall()
    return None if not values else [v.strip() for v in values]