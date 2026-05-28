import re

def split_into_sentences(text : str):
    # Remove === signs
    text = re.sub(r'===\s*[^=]+\s*===', '', text)
    # Improved regex pattern to split text into sentences
    sentence_endings = re.compile(r'(?<!\b\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s+(?=[A-Z])')
    sentences = sentence_endings.split(text.strip())
    return sentences

# helpers.py
def is_valid_sentence(doc, text: str) -> bool:
    words = text.split()
    if len(words) < 8 or len(words) > 50:
        return False
    if not text[0].isupper():
        return False
    if not text.rstrip().endswith(('.', '!', '?')):
        return False
    if any(kw in text.lower() for kw in [
        'subscribe', 'newsletter', 'sign up',
        'click here', 'read more', 'follow us'
    ]):
        return False

    # catch fragments like "decades later." or "Ages 1 month to 5 years."
    has_subject = any(t.dep_ in ('nsubj', 'nsubjpass') for t in doc)
    has_verb = any(t.pos_ == 'VERB' for t in doc)
    if not has_subject or not has_verb:
        return False

    return True