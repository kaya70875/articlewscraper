import spacy
import scrapy
import datetime
import logging

from config import config
from scripts.helpers import is_valid_sentence

logger = logging.getLogger(__name__)
nlp = spacy.load("en_core_web_sm")


class BaseArticleSpider(scrapy.Spider):
    """
    Base spider for scraping article pages and extracting validated sentences.

    Attributes:
        article_selector: CSS selector for paragraph-like elements.
            Must point to container elements such as `p`, not `::text` nodes,
            because `extract_article_sentences()` extracts text from inside them.
        next_page_selector: CSS selector for the next-page link.
        category: Category label stored on each extracted sentence.
        page_limit_key: Config key used to limit crawl depth.
        link_selector: CSS selector for article links on listing pages.
    """

    article_selector = None
    next_page_selector = None
    category = None
    page_limit_key = None
    link_selector = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = 0

    def setup_parse(self, response):
        if self.page >= getattr(config, self.page_limit_key):
            logger.info(
                "%s reached page limit at page %s",
                self.name,
                self.page
            )
            self.crawler.engine.close_spider(self, "Reached max. page count!")
            return

        links = response.css(self.link_selector).getall()

        if not links:
            logger.warning(
                "%s found no article links on %s",
                self.name,
                response.url
            )

        for link in links:
            next_url = response.urljoin(link)
            yield scrapy.Request(next_url, callback=self.parse_article)

        next_page = response.css(self.next_page_selector).get()
        self.page += 1

        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def extract_article_sentences(self, response):
        paragraph_nodes = response.css(self.article_selector)
        valid_sentences = []

        for p in paragraph_nodes:
            paragraph_text = " ".join(p.css("::text").getall()).strip()
            if not paragraph_text:
                continue

            doc = nlp(paragraph_text)

            for sent in doc.sents:
                sentence_text = sent.text.strip()
                if is_valid_sentence(sent, sentence_text):
                    valid_sentences.append(sentence_text)

        if not valid_sentences:
            logger.info(
                "%s produced no valid sentences for %s",
                self.name,
                response.url
            )
            return

        for i, text in enumerate(valid_sentences):
            yield {
                "text": text,
                "prev_sentence": valid_sentences[i - 1] if i > 0 else "",
                "next_sentence": valid_sentences[i + 1] if i < len(valid_sentences) - 1 else "",
                "source": response.url,
                "category": self.category,
                "length": len(text.split()),
                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            }