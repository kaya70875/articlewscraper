import argparse
from data import refactor
from scripts import word_algo

# ERROR YAKALAMAK İÇİN SPİDERLARI UPDATE DOSYASINDAN CRAWL VE RUN YAPMAMIZ GEREKİYOR ONU YAPMAYA ÇALIŞ İLK HEDEFİMİZ REACTORNOTRESTARTBLE HATASINI YAKALAMAK.

def main():
    parser = argparse.ArgumentParser(description="Generate sentences from web sources.")
    parser.add_argument('-s', '--sources', nargs='+', choices=['science', 'news', 'psy' , 'all'], required=True, help="Sources to create sentences from (choose from: science, news, psy[psychology] , all).")
    parser.add_argument('-l', '--length', type=int, default=100, help="Maximum length of the sentences.")
    parser.add_argument('-w', '--word', required=True, help="Word to search for in the sentences.")

    args = parser.parse_args()

    sources = []
    if 'science' in args.sources:
        sources.append(refactor.get_science())
    if 'news' in args.sources:
        sources.append(refactor.get_news())
    if 'psy' in args.sources:
        sources.append(refactor.get_psy())
    elif 'all' in args.sources:
        sources.append(refactor.get_science())
        sources.append(refactor.get_psy())
        sources.append(refactor.get_news())

    if len(sources) > 1:
        sentences = word_algo.create_topics(sources, args.word, max_length=args.length)
    else:
        sentences = word_algo.create_single_topic(sources[0], args.word, max_length=args.length)

    for i, sentence in enumerate(sentences):
        print(f'Sentence {i + 1}: {sentence}')

if __name__ == "__main__":
    main()
