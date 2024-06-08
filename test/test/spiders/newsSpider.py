import scrapy
import json
from scrapy.crawler import CrawlerProcess

from config import config

class BBCNews(scrapy.Spider):
    name = 'crawlbbcNews'
    start_urls = [
        'https://web-cdn.api.bbci.co.uk/xd/content-collection/b08a1d2f-6911-4738-825a-767895b8bfc4?country=tr&page=0&size=9',
        'https://web-cdn.api.bbci.co.uk/xd/content-collection/e2cc1064-8367-4b1e-9fb7-aed170edc48f?country=tr&page=0&size=9',
        'https://web-cdn.api.bbci.co.uk/xd/content-collection/db5543a3-7985-4b9e-8fe0-2ac6470ea45b?country=tr&page=0&size=9'
    ]

    custom_settings = {
        'FEEDS': {
            'data/news/bbcNews.json': {
                'format': 'json',
                'overwrite': True
            }
        }
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={'page': 0, 'base_url': url.split('?')[0]})

    def parse(self, response):
        current_page = response.meta['page']
        base_url = response.meta['base_url']

        if current_page >= config.BBC_PAGE:
            self.crawler.engine.close_spider(self, 'Reached max. page count!')

        data = json.loads(response.text)
        for item in data['data']:
            next_url = f'https://www.bbc.com{item["path"]}'
            yield scrapy.Request(next_url, callback=self.parse_article)

        next_page = current_page + 1
        next_page_url = f'{base_url}?country=tr&page={next_page}&size=9'
        
        if next_page < config.BBC_PAGE:
            yield scrapy.Request(next_page_url, callback=self.parse, meta={'page': next_page, 'base_url': base_url})

    def parse_article(self, response):
        body = response.css('p::text').getall()
        for text in body:
            yield {
                'text': text
            }

process = CrawlerProcess()
process.crawl(BBCNews)
