from test.spiders import scienceSpider, newsSpider, psySpider
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
import logging
from colorama import Fore, Style, init

logging.getLogger('scrapy').propagate = False
init()

def update():
    print(Fore.GREEN + 'Fetching websites... This could take about 2-15 minutes based on the number of pages being fetched.' + Style.RESET_ALL)

    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    runner.crawl(scienceSpider.CrawlLiveScience)
    runner.crawl(scienceSpider.CrawlScienceNews)
    runner.crawl(newsSpider.BBCNews)
    runner.crawl(psySpider.CrawlNeuroSc)

    d = runner.join()

    from twisted.internet import reactor
    d.addBoth(lambda _: reactor.stop())

    reactor.run()

if __name__ == '__main__':
    update()
    print(Fore.RED + 'Database updated sucsessfully!' + Style.RESET_ALL)
