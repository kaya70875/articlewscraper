from .base import BaseArticleSpider

class CrawlPsyh(BaseArticleSpider): #psychologytoday
    name = 'crawlpsyh'
    allowed_domains = ['psychologytoday.com']
    start_urls = ['https://www.psychologytoday.com/us/']

    page_limit_key = "PSYTODAY_PAGE"
    link_selector = 'h2.teaser-lg__title a::attr(href)'
    next_page_selector = 'a[rel="next"]::attr(href)'
    article_selector = 'div.field-name-body p'
    category = "psychology"

    def parse(self, response):
        yield from self.setup_parse(response)
            
    def parse_article(self, response):
        yield from self.extract_article_sentences(response)

class CrawlNeuroSc(BaseArticleSpider):
    name = 'crawlneuroScience'
    allowed_domains = ['neurosciencenews.com']
    start_urls = ['https://neurosciencenews.com/neuroscience-topics/psychology/']

    page_limit_key = "NEUROSCIENCE_PAGE"
    link_selector = 'div.title-wrap a::attr(href)'
    article_selector = 'div.entry-content.body-color.clearfix.link-color-wrap p'
    next_page_selector = 'a.next.page-numbers::attr(href)'
    category = "psychology"
    
    def parse(self, response):
        yield from self.setup_parse(response)
    
    def parse_article(self , response):
        yield from self.extract_article_sentences(response)
