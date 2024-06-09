# LearnWithArticles

## Overview

This project helps to understand english words better for creating sentences from diffirent articles and topics.

## Installation

### Prerequisites

- Python
- Pip

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/kaya70875/LearnWithArticles.git
   cd LearnWithArticles

    Install dependencies:

    pip install -r requirements.txt

Usage

    Configuration:
        Update the config.ini file to configure project settings such as file paths and spider parameters.

    Data Collection:
        Run the spiders to collect data from configured websites:

        You must update database first using 'python update.py'

        Crawled files stored inside data folder as .json file.

    Example Usage :
        'python update.py' for update database.
        main.py -s news science -l 100 -w make
    Example Usage 2 :
        main.py -s all -l 100 -w prevent

    Above code create sentences about 'make' from news related articles max 100 length of word.
