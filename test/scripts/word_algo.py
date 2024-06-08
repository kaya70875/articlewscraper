import re

def create_single_topic(topic, word: str, max_length: int = 100):
    sentences = []
    
    sentences.extend(re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', topic))
    
    keyword_sentences = [sentence for sentence in sentences if word in sentence and len(sentence) <= max_length]
    
    if not keyword_sentences:
        for sentence in sentences:
            if len(sentence) > max_length:
                keyword_sentences.extend(re.split(r'[;,]', sentence))
                
        keyword_sentences = [sentence for sentence in keyword_sentences if word in sentence and len(sentence) <= max_length]
    
    return keyword_sentences

def create_topics(topics: list, word: str, max_length: int = 100):
    sentences = []
    
    for topic in topics:
        sentences.extend(re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', topic))
    
    keyword_sentences = [sentence for sentence in sentences if word in sentence and len(sentence) <= max_length]
    
    if not keyword_sentences:
        for sentence in sentences:
            if len(sentence) > max_length:
                keyword_sentences.extend(re.split(r'[;,]', sentence))
                
        keyword_sentences = [sentence for sentence in keyword_sentences if word in sentence and len(sentence) <= max_length]
    
    return keyword_sentences
