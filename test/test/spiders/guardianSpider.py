import datetime
import logging
import scrapy
import spacy
from config import config
from scripts.helpers import is_valid_sentence

logger = logging.getLogger(__name__)
nlp = spacy.load("en_core_web_sm")

class TheGuardian(scrapy.Spider):
    name = "crawlGuardian"
    allowed_domains = ["theguardian.com"]
    categories = {
        "news": [
            "world",
            "uk/environment",
            "uk/technology",
            "uk/business",
        ],
        "sport": [
            "football",
            "sport/tennis",
            "sport/formulaone",
            "sport/golf",
        ],
        "lifestyle": [
            "fashion",
            "food",
            "tone/recipes",
            "lifeandstyle/health-and-wellbeing",
            "uk/travel",
            "lifeandstyle/family",
            "uk/money",
        ],
    }
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
    }
    page_limit = config.GUARDIAN_PAGE
    article_selector = ".article-body-commercial-selector p"

    def start_requests(self):
        # Iterate over subcategories so URLs are e.g. /world/all, /books/all
        # Carry the parent category (news/culture/sport/lifestyle) in meta
        for parent_category, subcategories in self.categories.items():
            for subcategory in subcategories:
                yield scrapy.Request(
                    url=f"https://www.theguardian.com/{subcategory}/all?page=0",
                    callback=self.parse,
                    meta={
                        "parent_category": parent_category,
                        "subcategory": subcategory,
                        "page": 0,
                    },
                )

    def parse(self, response):
        parent_category = response.meta["parent_category"]
        subcategory = response.meta["subcategory"]
        page = response.meta["page"]
        logger.info("Parsing %s/%s page %s", parent_category, subcategory, page)

        # Match links under the subcategory path (e.g. /world/...)
        article_links = response.css(
            f'main a[href^="/{subcategory}/"]:not([href*="?page="])::attr(href)'
        ).getall()

        if not article_links:
            logger.warning("No article links found on %s", response.url)

        for link in article_links:
            yield response.follow(
                link,
                callback=self.parse_article,
                meta={
                    "parent_category": parent_category,
                },
            )

        next_page = page + 1
        print("next page: " + str(next_page))

        if next_page >= self.page_limit:
            logger.info(
                "%s/%s reached page limit (%s)",
                parent_category,
                subcategory,
                self.page_limit,
            )
            return

        yield scrapy.Request(
            url=f"https://www.theguardian.com/{subcategory}/all?page={next_page}",
            callback=self.parse,
            meta={
                "parent_category": parent_category,
                "subcategory": subcategory,
                "page": next_page,
            },
        )

    def parse_article(self, response):
        # Resolve the correct parent category from meta instead of self.category
        parent_category = response.meta["parent_category"]

        paragraphs = response.css(self.article_selector)
        valid_sentences = []

        for paragraph in paragraphs:
            text = " ".join(paragraph.css("::text").getall()).strip()
            if not text:
                continue
            doc = nlp(text)
            for sent in doc.sents:
                sentence_text = sent.text.strip()
                if is_valid_sentence(sent, sentence_text):
                    valid_sentences.append(sentence_text)

        if not valid_sentences:
            return

        today = datetime.datetime.now().strftime("%Y-%m-%d")

        for i, text in enumerate(valid_sentences):
            yield {
                "text": text,
                "prev_sentence": valid_sentences[i - 1] if i > 0 else "",
                "next_sentence": (
                    valid_sentences[i + 1] if i < len(valid_sentences) - 1 else ""
                ),
                "source": response.url,
                "category": parent_category,
                "length": len(text.split()),
                "date": today,
            }