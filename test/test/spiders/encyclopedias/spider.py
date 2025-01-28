import scrapy
import datetime
from scripts.helpers import split_into_sentences
import json
import re
from config import config
import requests

def get_subjects():

    urls = []

    subjects = [
        "Artificial Intelligence", "Climate Change", "Quantum Physics",
        "World History", "Modern Art", "Space Exploration", "Genetics",
        "Philosophy", "Oceanography", "Cybersecurity", "Renewable Energy",
        "Machine Learning", "Robotics", "Psychology", "Economics",
        "Political Science", "Music Theory", "Astrophysics", "Linguistics",
        "Biotechnology", "Astronomy", "Architecture", "Sociology",
        "Environmental Science", "Mathematics", "Programming Languages",
        "Web Development", "Digital Marketing", "Blockchain Technology",
        "Data Science", "Health and Nutrition", "Entrepreneurship",
        "Cultural Anthropology", "Philosophy of Mind", "Neuroscience",
        "Artificial Neural Networks", "Photography", "Game Development",
        "Augmented Reality", "Ecology", "Ethics", "Nanotechnology",
        "Machine Vision", "Astronomy", "Cryptography", "Classical Music",
        "Creative Writing", "Biochemistry", "Environmental Conservation",
        "Public Speaking", "Software Engineering", "History of Science",
        "World Literature", "Bioinformatics", "Cognitive Science",
        "Forensic Science", "Space Technology", "Ecosystems",
        "Renewable Energy", "Paleontology", "Virtual Reality",
        "Cyber Ethics", "Renewable Resources", "Marine Biology",
        "Evolutionary Biology", "Game Theory", "Behavioral Economics",
        "Advanced Mathematics", "Historical Events", "Human Anatomy",
        "Pharmaceuticals", "Transportation Systems", "Social Media",
        "Digital Transformation", "World Mythology", "Theoretical Physics"
    ]

    for subject in subjects:
        base_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={subject.replace(' ' , '_')}&prop=extracts&format=json&explaintext"
        urls.append(base_url)

    return urls

def create_start_urls(count : int):
    url = []

    for _ in range(count):
        r = requests.get("https://www.wikihow.com/Special:Randomizer")
        url.append(r.url)
    return url

class WikipediaSpider(scrapy.Spider):
    name = 'wikipedia'

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    def start_requests(self):
        urls = get_subjects()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        pages = data.get('query', {}).get('pages', {})
        for page_id, page_info in pages.items():
            title = page_info.get('title', 'Unknown Title')
            content = page_info.get('extract', 'No content available')
            article_url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
        
            sentences = split_into_sentences(content)

            for sentence in sentences:
                yield {
                    'text': sentence,
                    'source': article_url,
                    'category': 'encyclopedia',
                    'length': len(sentence),
                    'date': datetime.datetime.now().strftime('%Y-%m-%d')
                }

class WikiHowSpider(scrapy.Spider):
    name = 'wikihow'

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }

    def start_requests(self):

        urls = create_start_urls(100)
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)
        
    def parse(self, response):
        content = response.css('.step::text').getall()
        
        # Join the content and clean up extra whitespace and newlines
        cleaned_content = " ".join(content).strip()
        cleaned_content = re.sub(r'\s+', ' ', cleaned_content)

        sentences = split_into_sentences(cleaned_content)
        for sentence in sentences:
            yield {
                'text': sentence,
                'source': response.url,
                'category': 'encyclopedia',
                'length': len(sentence),
                'date': datetime.datetime.now().strftime('%Y-%m-%d')
            }