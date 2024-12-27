from test.spiders import scienceSpider, newsSpider, psySpider
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
import logging
from colorama import Fore, Style, init
import time
from config.config import BBC_PAGE, PSYTODAY_PAGE, LIVESC_PAGE, SCIENCENEWS_PAGE, NEUROSCIENCE_PAGE
import argparse

logging.getLogger('scrapy').propagate = False
init()

def update(batch_size=100):
    print(Fore.GREEN + 'Fetching websites... This could take about 2-15 minutes based on the number of pages being fetched.' + Style.RESET_ALL)

    start_time = time.time()

    settings = get_project_settings()
    settings.set('BATCH_SIZE', batch_size)
    runner = CrawlerRunner(settings)

    runner.crawl(newsSpider.BBCNews)
    runner.crawl(scienceSpider.CrawlLiveScience)
    runner.crawl(scienceSpider.CrawlScienceNews)
    runner.crawl(psySpider.CrawlNeuroSc)

    d = runner.join()

    from twisted.internet import reactor
    d.addBoth(lambda _: reactor.stop())

    reactor.run()

    end_time = time.time()
    duration = end_time - start_time

    total_pages = sum([BBC_PAGE, PSYTODAY_PAGE, LIVESC_PAGE, SCIENCENEWS_PAGE, NEUROSCIENCE_PAGE])

    print(Fore.BLUE + f'Database updated successfully in {duration:.2f} seconds!' + Style.RESET_ALL)
    print(Fore.BLUE + f'Total of {total_pages} pages scraped!' + Style.RESET_ALL)
    print(f'Batch Size {batch_size}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update the database with new pages.')
    parser.add_argument('-b' , '--batch_size', type=int, default=100, required=False, help='Number of pages to fetch per batch.')
    args = parser.parse_args()
    update(args.batch_size)
