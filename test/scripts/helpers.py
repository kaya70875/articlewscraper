import re

def split_into_sentences(text : str):
    # Remove === signs
    text = re.sub(r'===\s*[^=]+\s*===', '', text)
    # Improved regex pattern to split text into sentences
    sentence_endings = re.compile(r'(?<!\b\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s+(?=[A-Z])')
    sentences = sentence_endings.split(text.strip())
    return sentences
