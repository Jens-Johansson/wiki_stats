#!/usr/bin/python3

#
# Check how many distinct language wiki pages exist for a person 
#
# Usage: ./wiki_count_languages.py [-h] <URL of personal page>
#
# NB, likely Goodhart's Law would apply to this if it ever 
# were to become some kind of common metric
#
# JJ v1 20260424 with some assistance from Z.ai GLM4.7 (reasoning)
#
# (c) 2-clause BSD
#

import requests
from urllib.parse import urlparse, unquote
import argparse

def get_qid(article_url):

    try:
        # 1. Parse the URL to extract language code and title
        parsed = urlparse(article_url)

        # Extract language (e.g., en.wikipedia.org -> en)
        domain_parts = parsed.netloc.split('.')
        if len(domain_parts) < 3 or 'wikipedia' not in parsed.netloc:
            print("Error: URL does not appear to be a valid Wikipedia link.")
            return None
        lang_code = domain_parts[0]

        # Extract title from path (e.g., /wiki/Albert_Einstein -> Albert_Einstein)
        path_parts = parsed.path.split('/')
        if len(path_parts) < 3 or path_parts[1] != 'wiki':
            print("Error: URL path format is incorrect. Expected /wiki/Page_Title.")
            return None

        title = unquote(path_parts[2])

        # 2. Use the MediaWiki API to get the 'wikibase_item' property (the QID)
        # Documentation: https://www.mediawiki.org/wiki/API:Query

        api_url = f"https://{lang_code}.wikipedia.org/w/api.php"

        params = {
            'action': 'query',
            'titles': title,
            'prop': 'pageprops',
            'ppprop': 'wikibase_item',
            'format': 'json'
        }

        # Identify the tool
        headers = {
            'User-Agent': 'WikiLangCountTool/1.0 (jens@panix.com)' 
        }

        response = requests.get(api_url, params=params, headers=headers)
        data = response.json()

        # 3. Extract the QID from the JSON response
        # The API returns a dictionary where the page ID is the key (usually a number).
        # We iterate to find the 'wikibase_item'.
        pages = data.get('query', {}).get('pages', {})

        for page_id, page_info in pages.items():
            if 'missing' in page_info:
                print(f"Error: The page '{title}' was not found on {lang_code} Wikipedia.")
                return None

            qid = page_info.get('pageprops', {}).get('wikibase_item')
            return qid

    except Exception as e:
        print(f"An error occurred while fetching QID: {e}")
        return None


def get_wikipedia_language_data(qid):

    url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"

    headers = {
        'User-Agent': 'WikiLangCountTool/1.0 (jens@panix.com)' 
    }

    wiki_urls = []

    # List of Wikimedia projects that are NOT Wikipedia.
    # We exclude these keys to ensure we only count Wikipedia versions.
    excluded_sites = [
        'wikidatawiki', 'commonswiki', 'wikisource', 'wikibooks', 
        'wikiquote', 'wikinews', 'wikiversity', 'wikivoyage', 'wiktionary'
    ]

    try:
        response = requests.get(url, headers=headers)

        # print(f"Status Code: {response.status_code}")
        if not response.text:
            print("Error: Empty resonse for ID {qid}")
            return 0, []

        data = response.json()

        # Access the sitelinks dictionary
        # Handles missing 'sitelinks' key gracefully
        sitelinks = data.get('entities', {}).get(qid, {}).get('sitelinks', {})

        for site_key, site_data in sitelinks.items():
            # Filter for Wikipedia domains (e.g., enwiki, dewiki)
            # Exclude special sites like commonswiki or wikidatawiki
            if site_key.endswith('wiki') and site_key not in excluded_sites:

                # 1. Get the language code (remove "wiki" from the end)
                # e.g., "enwiki" -> "en"
                lang_code = site_key.replace('wiki', '')

                # 2. Get the title from the sitelink data
                # Wikidata titles usually use underscores (e.g., "New_York")
                # Spaces are replaced by underscores for valid URLs
                title = site_data.get('title', '').replace(' ', '_')

                # 3. Construct the URL
                full_url = f"https://{lang_code}.wikipedia.org/wiki/{title}"

                wiki_urls.append(full_url)

        return len(wiki_urls), wiki_urls

    except Exception as e:
        print(f"An error occurred: {e}")
        return 0, []


def main():
    parser = argparse.ArgumentParser(description="Count Wikipedia language pages for an individual.")
    parser.add_argument("url", help="The Wikipedia article URL (e.g., https://en.wikipedia.org/wiki/Douglas_Adams)")

    args = parser.parse_args()

    print(f"Processing URL: {args.url}")

    qid = get_qid(args.url)

    if not qid:
        print("Could not find a QID for that URL.")
        return

    print(f"Found Wikidata ID: {qid}")

    count, urls = get_wikipedia_language_data(qid)

    for u in urls:
        print(u)

    print(f"\nTotal distinct language pages: {count}")

if __name__ == "__main__":
    main()
