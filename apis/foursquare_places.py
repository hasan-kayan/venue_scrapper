import requests
import os
from dotenv import load_dotenv

load_dotenv()
FOURSQUARE_API_KEY = os.getenv("FOURSQUARE_API_KEY")

def search_places_foursquare(location):
    url = "https://api.foursquare.com/v3/places/search"
    headers = {"Authorization": FOURSQUARE_API_KEY}
    params = {
        "query": "restaurant",
        "near": location,
        "limit": 50
    }

    response = requests.get(url, headers=headers, params=params).json()
    venues = []

    for result in response.get("results", []):
            print("🔍 Raw venue:", result)

            name = result.get("name", "")
            description = result.get("categories", [{}])[0].get("name", "")
            location = result.get("location", {}).get("formatted_address", "")
            rating = result.get("rating", "")

            venues.append({
                "name": name,
                "description": description,
                "category": "Foursquare",
                "location": location,
                "rating": rating
            })



    return venues
