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
   git clone https://github.com/your_username/your_project.git
   cd LearnWithArticles

    Install dependencies:

    bash

    pip install -r requirements.txt

Usage

    Configuration:
        Update the config.ini file to configure project settings such as file paths and spider parameters.

    Data Collection:
        Run the spiders to collect data from configured websites:

        You must use -u parameter for first time running.

        Crawled files stored inside data folder as .json file.

    Example Usage :
        main.py -h for help
        main.py -u -s news -l 100 -w make
        main.py -s news science -l 200 -w make

    Above code updates the database and create sentences about 'make' from news related articles max 100 length of word.
    For the second time You don't have to update database.
