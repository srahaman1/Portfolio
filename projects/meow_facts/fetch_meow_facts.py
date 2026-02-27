"""
fetch_meow_facts.py

Fetches cat facts from the Meowfacts API in every supported language
and saves them to a local JSON file called cat_facts.json.

Runs once per day — if the output file already contains today's data,
the API calls are skipped entirely.

API:      https://meowfacts.herokuapp.com/
Usage:    python fetch_meow_facts.py
Requires: pip install requests
"""

import json
import os
import requests
from datetime import date


# --- Configuration -----------------------------------------------------------

API_BASE_URL = "https://meowfacts.herokuapp.com"

# The output file is saved in the same folder as this script
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cat_facts.json")


# --- Helper functions --------------------------------------------------------

def get_available_languages():
    """
    Call the /options endpoint to get every supported language.
    Returns a list of language objects, each containing:
      - iso_code    (e.g. "eng-us")  — the code to pass to the facts endpoint
      - english_name (e.g. "english")
      - fact_count  (e.g. 90)        — the exact number of facts in that language
    Returns an empty list if the request fails.
    """
    url = API_BASE_URL + "/options"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        payload = response.json()
        languages = payload.get("lang", [])
        return languages

    except requests.exceptions.ConnectionError:
        print("[ERROR] No internet connection. Cannot reach the API.")
        return []
    except requests.exceptions.Timeout:
        print("[ERROR] Request to /options timed out.")
        return []
    except requests.exceptions.HTTPError as err:
        print(f"[ERROR] HTTP error from /options: {err}")
        return []
    except Exception as err:
        print(f"[ERROR] Unexpected error from /options: {err}")
        return []


def fetch_facts_for_language(iso_code, fact_count):
    """
    Fetch all facts for one language from the Meowfacts API.

    iso_code   — language code like "eng-us" or "rus-ru"
    fact_count — how many facts exist for this language (from /options)

    Returns a list of fact strings, or an empty list if the request fails.
    """
    url = API_BASE_URL + "/"
    params = {
        "lang": iso_code,
        "count": fact_count,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        payload = response.json()
        facts = payload.get("data", [])
        return facts

    except requests.exceptions.ConnectionError:
        print(f"  [ERROR] No internet connection while fetching '{iso_code}'.")
        return []
    except requests.exceptions.Timeout:
        print(f"  [ERROR] Request timed out for '{iso_code}'.")
        return []
    except requests.exceptions.HTTPError as err:
        print(f"  [ERROR] HTTP error for '{iso_code}': {err}")
        return []
    except Exception as err:
        print(f"  [ERROR] Unexpected error for '{iso_code}': {err}")
        return []


def load_existing_data():
    """
    Read cat_facts.json from disk and return its contents as a dictionary.
    Returns None if the file does not exist or cannot be parsed.
    """
    if not os.path.exists(OUTPUT_FILE):
        return None

    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("Warning: existing file is corrupted. Will re-fetch data.")
            return None

    return data


def is_data_from_today(data):
    """
    Return True if the data was already fetched today, False otherwise.
    The 'date' field in the JSON is compared to today's date (YYYY-MM-DD).
    """
    today = str(date.today())
    return data.get("date") == today


def save_data(all_facts):
    """
    Write the collected facts to cat_facts.json.
    The output includes today's date so future runs can detect fresh data.
    """
    output = {
        "date": str(date.today()),
        "languages": all_facts,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        # ensure_ascii=False preserves non-Latin characters (Korean, Russian, etc.)
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nSaved to: {OUTPUT_FILE}")


def print_summary(all_facts):
    """Print how many facts were collected per language."""
    print("\n--- Summary ---")
    total = 0
    for lang_code, facts in all_facts.items():
        count = len(facts)
        total += count
        print(f"  {lang_code}: {count} fact(s)")
    print(f"\n  Total: {total} fact(s) across {len(all_facts)} language(s)")


# --- Entry point -------------------------------------------------------------

if __name__ == "__main__":
    print("=== Meowfacts Daily Fetcher ===\n")

    # Step 1: Check if today's data already exists
    existing_data = load_existing_data()

    if existing_data is not None and is_data_from_today(existing_data):
        print("Data is already up to date for today. Nothing to fetch.")
        print(f"File : {OUTPUT_FILE}")
        print(f"Date : {existing_data['date']}")
        print_summary(existing_data["languages"])
        print("\nDone.")

    else:
        # Step 2: Find out which languages are available and how many facts each has
        if existing_data is None:
            print("No existing data found. Fetching for the first time...\n")
        else:
            print(f"Existing data is from {existing_data.get('date', 'unknown')}. Refreshing...\n")

        print("Fetching available languages from /options ...")
        languages = get_available_languages()

        if not languages:
            print("\n[ERROR] Could not retrieve language list. Exiting.")

        else:
            print(f"Found {len(languages)} language(s).\n")

            # Step 3: Fetch all facts for each language
            all_facts = {}

            for language in languages:
                iso_code = language.get("iso_code", "")
                fact_count = language.get("fact_count", 1)
                english_name = language.get("english_name", "")

                print(f"  Fetching {fact_count} fact(s) for {english_name} ({iso_code}) ...")
                facts = fetch_facts_for_language(iso_code, fact_count)
                all_facts[iso_code] = facts
                print(f"    -> Received {len(facts)} fact(s).")

            # Step 4: Save to JSON
            save_data(all_facts)

            # Step 5: Print a summary
            print_summary(all_facts)

            print("\nDone.")
