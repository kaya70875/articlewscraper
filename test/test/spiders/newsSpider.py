import scrapy
import json
import logging
from config import config
from .base import BaseArticleSpider

class BBCNews(BaseArticleSpider):
    name = 'crawlbbcNews'
    start_urls = [
        'https://web-cdn.api.bbci.co.uk/xd/content-collection/b08a1d2f-6911-4738-825a-767895b8bfc4?page=0&size=9', # News
        'https://web-cdn.api.bbci.co.uk/xd/content-collection/e2cc1064-8367-4b1e-9fb7-aed170edc48f?page=0&size=9', # News
        'https://web-cdn.api.bbci.co.uk/xd/content-collection/092c7c94-aa9b-4933-9349-eb942b3bde77?page=0&size=9', # Technology
        'https://web-cdn.api.bbci.co.uk/xd/content-collection/98529df5-2749-4618-844f-96431b3084d9?page=0&size=9', # Travel
        'https://web-cdn.api.bbci.co.uk/xd/content-collection/6ddbca4a-80f3-4875-8dd7-cbe76fca05b8?page=0&size=9' # Travel
        'https://web-cdn.api.bbci.co.uk/xd/content-collection/daa2a2f9-0c9e-4249-8234-bae58f372d82?page=0&size=9', # Business
        'https://web-cdn.api.bbci.co.uk/xd/content-collection/3da03ce0-ee41-4427-a5d9-1294491e0448?page=0&size=9', # Innovation
        'https://web-cdn.api.bbci.co.uk/xd/content-collection/6d50eb9d-ee20-40fe-8e0f-f506d6a02b78?page=0&size=9', # Culture
        'https://web-cdn.api.bbci.co.uk/xd/content-collection/ef20229c-cde4-449f-b225-6db94953d2ce?page=0&size=9', # Arts
        'https://web-cdn.api.bbci.co.uk/xd/content-collection/9f0b9075-b620-4859-abdc-ed042dd9ee66?page=0&size=9', # Earth
        'https://web-cdn.api.bbci.co.uk/xd/content-collection/6d032332-6ce5-425b-85a6-f260355718b3?page=0&size=9', # AI News

    ]

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    article_selector = 'p'
    category = "news"

    try:

        def start_requests(self):
            for url in self.start_urls:
                yield scrapy.Request(url, callback=self.parse, meta={'page': 0, 'base_url': url.split('?')[0]})

        def parse(self, response):
            current_page = response.meta['page']
            base_url = response.meta['base_url']

            logging.info(f'Parsing page {current_page} of {base_url}')

            if current_page >= config.BBC_PAGE:
                logging.info('Reached max. page count!')
                self.crawler.engine.close_spider(self, 'Reached max. page count!')

            data = json.loads(response.text)
            if 'data' not in data:
                logging.error('No data found in response')
                return

            for item in data['data']:
                next_url = f'https://www.bbc.com{item["path"]}'
                yield scrapy.Request(next_url, callback=self.parse_article)

            next_page = current_page + 1
            next_page_url = f'{base_url}?page={next_page}&size=9'
            if next_page_url:
                yield scrapy.Request(next_page_url, callback=self.parse, meta={'page': next_page, 'base_url': base_url})

        def parse_article(self, response):
            yield from self.extract_article_sentences(response)
    except TypeError as type_err:
        logging.error(f'TypeError in newsSpider: {type_err}')
