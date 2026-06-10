#!/usr/bin/python3

#
# Determine how many distinct humans are on Wikipedia
#
# Usage: ./wiki_count_humans.py [-h]
#
# JJ v1 20260424 with some assistance from Z.ai GLM4.7 (reasoning)
#
# (c) 2-clause BSD
#


import requests

def get_total_human_count():
    """
    Returns the total number of QIDs that are instances of 'human' (Q5).
    """
    # The Wikidata Query Service Endpoint
    url = "https://query.wikidata.org/sparql"

    # The SPARQL query to count all items of class Q5 (human)
    query = """
    SELECT (COUNT(?item) AS ?count)
    WHERE {
      ?item wdt:P31 wd:Q5 .
    }
    """

    # SPARQL queries require specific headers for JSON responses
    headers = {
        'User-Agent': 'MyWikiTool/1.0 (your_email@example.com)',
        'Accept': 'application/json'
    }

    try:
        # We use 'params' to pass the query string
        response = requests.get(url, params={'query': query, 'format': 'json'}, headers=headers)
        response.raise_for_status()

        data = response.json()

        # Extract the count from the results
        # The result is in data['results']['bindings'][0]['count']['value']
        count = data['results']['bindings'][0]['count']['value']

        return int(count)

    except Exception as e:
        print(f"Error fetching count: {e}")
        return None

# Example usage
count = get_total_human_count()
if count is not None:
    print(f"Total non-fictional persons (QIDs): {count}")
