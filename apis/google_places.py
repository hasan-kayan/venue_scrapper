import requests
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def search_places_google(location):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"restaurants in {location}",
        "key": GOOGLE_API_KEY
    }
    response = requests.get(url, params=params).json()
    venues = []

    for result in response.get("results", []):
        venues.append({
            "name": result.get("name"),
            "description": result.get("types"),
            "category": "Google",
            "location": result.get("formatted_address"),
            "rating": result.get("rating")
        })

    return venues
