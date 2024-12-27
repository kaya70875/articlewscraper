import configparser

config = configparser.ConfigParser()
config.read('config.ini')
# PAGE VALUES FOR SPIDERS : 

BBC_PAGE = config['DEFAULT'].getint('BBC_PAGE') #bbcnews.com
PSYTODAY_PAGE = config['DEFAULT'].getint('PSYTODAY_PAGE') #psychologytoday.com/us
LIVESC_PAGE = config['DEFAULT'].getint('LIVESC_PAGE') # livescience.com / be careful with this there is so many links in one page!
SCIENCENEWS_PAGE = config['DEFAULT'].getint('SCIENCENEWS_PAGE') #sciencenews.com / this one may require high number.
NEUROSCIENCE_PAGE = config['DEFAULT'].getint('NEUROSCIENCE_PAGE') #neuroscience.com
