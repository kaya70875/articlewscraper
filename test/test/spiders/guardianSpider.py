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
            "environment",
            "technology",
            "business",
        ],
        "sport": [
            "football",
            #"sport/tennis",
            #"sport/formulaone",
            #"sport/golf",
        ],
        "lifestyle": [
            "fashion",
            "food",
            "travel",
            "money"
            #"lifeandstyle/health-and-wellbeing",
            #"lifeandstyle/family",
        ],
    }
    custom_settings = {
        "ROBOTSTXT_OBEY": False,
    }
    page_limit = config.GUARDIAN_PAGE
    article_selector = ".article-body-commercial-selector p"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tracks { parent_category: { subcategory: article_count } }
        self.article_counts = {
            parent: {sub: 0 for sub in subs}
            for parent, subs in self.categories.items()
        }

    def start_requests(self):
        total_subcategories = sum(len(v) for v in self.categories.values())
        logger.info(
            "Starting crawl: %d parent categories, %d subcategories, page limit %d",
            len(self.categories),
            total_subcategories,
            self.page_limit,
        )
        for parent_category, subcategories in self.categories.items():
            for subcategory in subcategories:
                logger.info(
                    "Queuing subcategory [%s] under parent [%s]",
                    subcategory,
                    parent_category,
                )
                yield scrapy.Request(
                    url=f"https://www.theguardian.com/{subcategory}/all?page=1",
                    callback=self.parse,
                    meta={
                        "parent_category": parent_category,
                        "subcategory": subcategory,
                        "page": 1,
                    },
                )

    def parse(self, response):
        parent_category = response.meta["parent_category"]
        subcategory = response.meta["subcategory"]
        page = response.meta["page"]

        article_links = response.css(
            f'main a[href^="/{subcategory}/"]:not([href*="?page="])::attr(href)'
        ).getall()

        if not article_links:
            logger.warning(
                "[%s/%s] Page %d — no article links found (url: %s)",
                parent_category,
                subcategory,
                page,
                response.url,
            )
        else:
            logger.info(
                "[%s/%s] Page %d — found %d article links",
                parent_category,
                subcategory,
                page,
                len(article_links),
            )

        for link in article_links:
            yield response.follow(
                link,
                callback=self.parse_article,
                meta={
                    "parent_category": parent_category,
                    "subcategory": subcategory,
                },
            )

        next_page = page + 1
        if next_page >= self.page_limit:
            logger.info(
                "[%s/%s] Reached page limit (%d), stopping.",
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
        parent_category = response.meta["parent_category"]
        subcategory = response.meta["subcategory"]

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
            logger.warning(
                "[%s/%s] No valid sentences extracted from %s",
                parent_category,
                subcategory,
                response.url,
            )
            return

        logger.info(
            "[%s/%s] Scraped %d sentences from %s",
            parent_category,
            subcategory,
            len(valid_sentences),
            response.url,
        )
        self.article_counts[parent_category][subcategory] += 1

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

    def closed(self, reason):
        logger.info("Spider closed: %s", reason)
        logger.info("===== Crawl Summary =====")
        for parent_category, subcategories in self.article_counts.items():
            total = sum(subcategories.values())
            logger.info(
                "[%s] total articles: %d",
                parent_category,
                total,
            )
            for subcategory, count in subcategories.items():
                if count == 0:
                    logger.warning(
                        "  [%s/%s] 0 articles fetched — check URL or selector",
                        parent_category,
                        subcategory,
                    )
                else:
                    logger.info("  [%s/%s] %d articles", parent_category, subcategory, count)
        logger.info("=========================")