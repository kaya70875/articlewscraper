import argparse
import logging
from data import refactor
from scripts import word_algo
from test.spiders import scienceSpider, newsSpider, psySpider

logging.getLogger('scrapy').propagate = False

def update_database():
    print('Fetching websites... This could take about 2-15 minutes based on the number of pages being fetched.')
    scienceSpider.process.start()
    newsSpider.process.start()
    psySpider.process.start()

def main():
    parser = argparse.ArgumentParser(description="Generate sentences from web sources.")
    parser.add_argument('-u', '--update', action='store_true', help="Update the database by fetching websites.")
    parser.add_argument('-s', '--sources', nargs='+', choices=['science', 'news', 'psy'], required=True, help="Sources to create sentences from (choose from: science, news, psy).")
    parser.add_argument('-l', '--length', type=int, default=100, help="Maximum length of the sentences.")
    parser.add_argument('-w', '--word', required=True, help="Word to search for in the sentences.")

    args = parser.parse_args()

    if args.update:
        update_database()

    sources = []
    if 'science' in args.sources:
        sources.append(refactor.get_science())
    if 'news' in args.sources:
        sources.append(refactor.get_news())
    if 'psy' in args.sources:
        sources.append(refactor.get_psy())

    if len(sources) > 1:
        sentences = word_algo.create_topics(sources, args.word, max_length=args.length)
    else:
        sentences = word_algo.create_single_topic(sources[0], args.word, max_length=args.length)

    for i, sentence in enumerate(sentences):
        print(f'Sentence {i + 1}: {sentence}')

if __name__ == "__main__":
    main()
