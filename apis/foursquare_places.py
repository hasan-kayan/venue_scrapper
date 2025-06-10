import requests
import os
from dotenv import load_dotenv

load_dotenv()
FOURSQUARE_API_KEY = os.getenv("FOURSQUARE_API_KEY")

DIET_QUERIES = {
    "gluten_free.csv": "gluten free restaurant",
    "vegan_vegetarian.csv": "vegan restaurant",
    "kosher.csv": "kosher restaurant"
}

def search_places_foursquare(location):
    url = "https://api.foursquare.com/v3/places/search"
    headers = {"Authorization": FOURSQUARE_API_KEY}
    all_results = []

    for filename, query in DIET_QUERIES.items():
        params = {
            "query": query,
            "near": location,
            "limit": 50
        }
        response = requests.get(url, headers=headers, params=params).json()
        print(f"🔍 {query.title()} → Found: {len(response.get('results', []))} venues in {location}")

        for result in response.get("results", []):
            venue = {
                "name": result.get("name", ""),
                "description": result.get("categories", [{}])[0].get("name", ""),
                "category": "Foursquare",
                "location": result.get("location", {}).get("formatted_address", ""),
                "rating": result.get("rating", ""),
                "target_csv": filename
            }
            all_results.append(venue)

    return all_results
