import re

def create_sentence(text , word):

    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

    keyword_sentences = [sentence for sentence in sentences if word in sentence]

    return keyword_sentences

def create_topics(topics : list , word):
    text = ''

    for topic in topics:
        text += topic + '\n'
    
    sentences = re.split(r'(?<!\w\.\w.)(?<![wA-Z][a-z]\.)(?<=\.|\?)\s', text)

    keyword_sentences = [sentence for sentence in sentences if word in sentence]

    return keyword_sentences