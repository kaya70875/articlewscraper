import scrapy
import datetime
from config import config
from .base import BaseArticleSpider

class CrawlScienceNews(BaseArticleSpider):
    name = "crawlscienceNews"
    allowed_domains = ["sciencenews.org"]
    start_urls = ["https://www.sciencenews.org/all-stories/"]

    article_selector = "div.rich-text.rich-text--with-sidebar.single__rich-text___RmCDp p"
    next_page_selector = "a.next.page-numbers::attr(href)"
    link_selector = "h3.post-item-river__title___vyz1w a::attr(href)"
    page_limit_key = "SCIENCENEWS_PAGE"
    category = "science"

    def parse(self, response):
        yield from self.setup_parse(response)

    def parse_article(self, response):
        yield from self.extract_article_sentences(response)

class CrawlLiveScience(BaseArticleSpider):
    name = "crawlliveScience"
    allowed_domains = ["livescience.com"]

    category = "science"
    page_limit_key = "LIVESC_PAGE"
    article_selector = "div.text-copy.bodyCopy.auto p"
    link_selector = "li.day-article a::attr(href)"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date = datetime.datetime.now()
        self.start_urls = [
            f"https://www.livescience.com/archive/{self.date.year}/{self.date.month:02d}"
        ]

    def parse(self, response):
        if self.page >= config.LIVESC_PAGE:
            self.crawler.engine.close_spider(self, "Reached max. page count!")
            return

        links = response.css(self.link_selector).getall()

        for link in links:
            next_url = response.urljoin(link)
            yield scrapy.Request(next_url, callback=self.parse_article)

        self.page += 1

        if self.page < config.LIVESC_PAGE:
            self.date = self.date.replace(day=1) - datetime.timedelta(days=1)
            next_page_url = f"https://www.livescience.com/archive/{self.date.year}/{self.date.month:02d}"
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_article(self, response):
        yield from self.extract_article_sentences(response)