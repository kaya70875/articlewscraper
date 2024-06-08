import scrapy
from config import config

class CrawlNYTravel(scrapy.Spider):
    name = 'crawlNYTravel'
    start_urls = ['https://www.nytimes.com/international/section/travel']
    page = 0

    custom_settings= {
            'FEEDS' : {'data/travel/travelSkift.json' : {'format' : 'json',
                                                  'overwrite' : True}}
        }

    def parse(self, response):
        self.page +=1
        if self.page > config.NYTRAVEL_PAGE:
            self.crawler.engine.close_spider(self, 'Reached max. page count!')
        
        links = response.css('a.css-8hzhxf::attr(href)').getall()

        for link in links:
            next_page = response.urljoin(link)
            yield scrapy.Request(next_page , callback=self.parse_article)
    
    
    def parse_article(self, response):
        pass
        
