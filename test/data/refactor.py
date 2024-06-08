from scripts import json_reader
from config import config

def get_science():

    liveScience = json_reader.extract_body(f'{config.JSON_FILE_PATH}/science/liveScience.json')
    scienceNews = json_reader.extract_body(f'{config.JSON_FILE_PATH}/science/scienceNews.json')

    all_science = liveScience + scienceNews

    return all_science

def get_news():

    bbcNews = json_reader.extract_body(f'{config.JSON_FILE_PATH}/news/bbcNews.json')

    return bbcNews

def get_psy():

    psyToday = json_reader.extract_body(f'{config.JSON_FILE_PATH}/psy/psyToday.json')
    neuroScience = json_reader.extract_body(f'{config.JSON_FILE_PATH}/psy/neuroScience.json')

    all_psy = psyToday + neuroScience

    return all_psy