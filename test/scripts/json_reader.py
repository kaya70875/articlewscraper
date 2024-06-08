import json

# Function to extract headers and count them
def extract_body(json_file_path):

    all_text = ''
    
    with open(json_file_path , 'r' , encoding='utf-8') as file:
        data = json.load(file)

        text = [entry['text'] for entry in data if 'text' in entry]

        for t in text:
            all_text += t
        
        return all_text
    