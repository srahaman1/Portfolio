import requests
from datetime import date
import json
import os

if __name__ == "__main__":
    
# output_file = 'path/to/cat_facts.json'
output_file = 'cat_facts.json'
# Check if the output file already exists and if it was created today
existing_data = json.load(open(output_file)) if os.path.exists(output_file) else None

# Check if the existing data is up to date: created today
if existing_data is not None and existing_data.get("date") == str(date.today()):
    print(f"Data in {output_file} is up to date.")

# if not up to date, pull new data and save/overwrite to file
else:
    if existing_data is None:
        print(f"Creating new data in {output_file}")
    else:
        print(f"Last updated: {existing_data['date']}")

    ## Pull metadata about available languages and fact counts
    url="https://meowfacts.herokuapp.com"
    url_meta=f'{url}/options'

    response = requests.get(url_meta)
    # response.raise_for_status()  # Check if the request was successful
    metadata = response.json()
    languages = metadata['lang']

    ## Pull all facts for each language and store them in a dictionary
    all_facts = {}

    for lang in languages:
        iso_code = lang['iso_code']  # Check if the language is English
        fact_count = lang['fact_count']
        english_name = lang['english_name']
        print(f"\nFetching {fact_count} fact(s) for {english_name} - {iso_code}")
            
        params = {
            'lang': iso_code,
            'count': fact_count
        }

        response = requests.get(url, params=params)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        facts = data['data']
        all_facts[iso_code] = facts
        print(f"Received {len(facts)} fact(s).")

    ## add date and all facts to a dictionary for output
    output = {
        "date": str(date.today()),
        "languages": all_facts
    }

    ## Save all facts to a JSON file
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=4)
    print(f"\nAll facts have been saved to {output_file}.")
