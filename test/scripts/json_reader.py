import json
import sys

# Function to extract headers and count them
def extract_body(json_file_path):

    all_text = ''
    try:
        with open(json_file_path , 'r' , encoding='utf-8') as file:
            data = json.load(file)

            text = [entry['text'] for entry in data if 'text' in entry]

            for t in text:
                all_text += t
            
            return all_text
    
    except(FileNotFoundError):
        print('Source file not found. Make sure you update database by writing "python update.py" or check your "config.ini" file folder path.')
        sys.exit(1)
    