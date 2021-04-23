import re
import tqdm
import scrapy

MOBY_BASE = 'https://www.mobygames.com'
MOBY_PLATFORM_DICTIONARY = {
    '3ds': '3ds',
    'dreamcast': 'dreamcast',
    'ds': 'ds',
    'game-boy-advance': 'gameboy-advance',
    'gamecube': 'gamecube',
    'nintendo-64': 'n64',
    'pc': 'windows',
    'playstation-2': 'ps2',
    'playstation-3': 'ps3',
    'playstation-4': 'playstation-4',
    'playstation-5': 'playstation-5',
    'playstation-vita': 'ps-vita',
    'playstation': 'playstation',
    'psp': 'psp',
    'stadia': 'stadia',
    'switch': 'switch',
    'wii-u': 'wii-u',
    'wii': 'wii',
    'xbox-360': 'xbox360',
    'xbox-one': 'xbox-one',
    'xbox-series-x': 'xbox-series',
    'xbox': 'xbox',
}

REGEX_EXPRESSION = re.compile(r"\((.*?)\)")

def pbar(count):
    params = dict(desc='Scraping', unit='game', ascii=True)
    return tqdm.tqdm(total=count, **params)

def platform(game):
    for left, right in MOBY_PLATFORM_DICTIONARY.items():
        if left in game: return game.replace(left, right)

def parse_url(game_list, subdir=''):
    expression = lambda x: MOBY_BASE + platform(x)
    return [expression(d + subdir) for d in game_list]

def extract_image_urls(response):
    values = response.xpath(f'//a[contains(@title, "Front Cover")]/@style').getall()
    return [MOBY_BASE + REGEX_EXPRESSION.search(value).group(1).replace('/s/', '/l/') for value in values]