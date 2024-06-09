from test.spiders import scienceSpider, newsSpider, psySpider
import logging
from colorama import Fore, Style, init

logging.getLogger('scrapy').propagate = False
init()

def update():
    print(Fore.GREEN + 'Fetching websites... This could take about 2-15 minutes based on the number of pages being fetched.' + Style.RESET_ALL)
    scienceSpider.process.start()
    newsSpider.process.start()
    psySpider.process.start()
if __name__ == '__main__':
    update()
    print(Fore.RED + 'Database updated sucsessfully!' + Style.RESET_ALL)
