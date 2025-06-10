import requests
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

DIET_QUERIES = {
    "gluten_free.csv": "gluten free restaurant",
    "vegan_vegetarian.csv": "vegan restaurant",
    "kosher.csv": "kosher restaurant"
}

def search_places_google(location):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    all_results = []

    for filename, query in DIET_QUERIES.items():
        params = {
            "query": f"{query} in {location}",
            "key": GOOGLE_API_KEY
        }
        response = requests.get(url, params=params).json()
        print(f"🔍 {query.title()} → Found: {len(response.get('results', []))} venues in {location}")

        for result in response.get("results", []):
            venue = {
                "name": result.get("name", ""),
                "description": " ".join(result.get("types", [])),
                "category": "Google",
                "location": result.get("formatted_address", ""),
                "rating": result.get("rating", ""),
                "target_csv": filename
            }
            all_results.append(venue)

    return all_results
