import scrapy
from scrapy.crawler import CrawlerProcess
from config import config
import datetime

class CrawlPsyh(scrapy.Spider): #psychologytoday
    name = 'crawlpsyh'
    allowed_domains = ['psychologytoday.com']
    start_urls = ['https://www.psychologytoday.com/us/']
    page = 0

    def parse(self, response):
        if self.page >= config.PSYTODAY_PAGE:
            self.crawler.engine.close_spider(self , 'Reached max. page count!')

        links = response.css('h2.teaser-lg__title a::attr(href)').getall()
        for link in links:
            next_url = response.urljoin(link)
            yield scrapy.Request(next_url, callback=self.parse_article)
        

        next_page = response.css('a[rel="next"]::attr(href)').get()
        self.page += 1
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)
            
    def parse_article(self, response):
        body = response.css('div.field-name-body')
        all_text = body.css('p::text').getall()
        for text in all_text:
            yield{
                'text' : text,
                'source' : response.url,
                'category' : 'psychology',
                'length' : len(text),
                'date' : datetime.datetime.now().strftime('%Y-%m-%d')
            }

class CrawlNeuroSc(scrapy.Spider):
    name = 'crawlneuroScience'
    start_urls = ['https://neurosciencenews.com/neuroscience-topics/psychology/']
    page = 0

    def parse(self, response):
        if self.page >= config.NEUROSCIENCE_PAGE:
            self.crawler.engine.close_spider(self , 'Reached max. page count!')
        
        links = response.css('div.title-wrap a::attr(href)').getall()

        for link in links:
            next_url = response.urljoin(link)
            yield scrapy.Request(next_url , callback=self.parse_article)
        
        next_page = response.css('a.next.page-numbers::attr(href)').get()
        self.page += 1
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url , callback=self.parse)
    
    def parse_article(self , response):
        body = response.css('div.entry-content.body-color.clearfix.link-color-wrap p::text').getall()
        for text in body:
            yield{
                'text' : text,
                'source' : response.url,
                'category' : 'psychology',
                'length' : len(text),
                'date' : datetime.datetime.now().strftime('%Y-%m-%d')
            }


process = CrawlerProcess()

process.crawl(CrawlPsyh)
process.crawl(CrawlNeuroSc)
