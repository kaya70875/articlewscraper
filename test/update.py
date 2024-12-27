from test.spiders import scienceSpider, newsSpider, psySpider
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
import logging
from colorama import Fore, Style, init
import time
from config.config import BBC_PAGE, PSYTODAY_PAGE, LIVESC_PAGE, SCIENCENEWS_PAGE, NEUROSCIENCE_PAGE

logging.getLogger('scrapy').propagate = False
init()

def update():
    print(Fore.GREEN + 'Fetching websites... This could take about 2-15 minutes based on the number of pages being fetched.' + Style.RESET_ALL)

    start_time = time.time()

    settings = get_project_settings()
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

if __name__ == '__main__':
    update()
