import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
FOURSQUARE_API_KEY = os.getenv("FOURSQUARE_API_KEY")

def load_filters():
    with open("config/filters.json", "r", encoding="utf-8") as f:
        return json.load(f)

DIET_FILTERS = load_filters()

def get_tips_for_place(fsq_id):
    url = f"https://api.foursquare.com/v3/places/{fsq_id}/tips"
    headers = {
        "Authorization": FOURSQUARE_API_KEY,
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        tips_data = response.json()
        if isinstance(tips_data, list):
            return [tip.get("text", "").lower() for tip in tips_data if "text" in tip]
        else:
            print(f"⚠️ Unexpected tips format for {fsq_id}: {tips_data}")
            return []
    except Exception as e:
        print(f"❌ Error fetching tips for {fsq_id}: {e}")
        return []


def search_places_foursquare(location):
    url = "https://api.foursquare.com/v3/places/search"
    headers = {
        "Authorization": FOURSQUARE_API_KEY,
        "Accept": "application/json"
    }

    search_categories = ["restaurant", "cafe", "bar"]
    all_results = []

    for category in search_categories:
        params = {
            "query": category,
            "near": location,
            "limit": 50
        }

        response = requests.get(url, headers=headers, params=params).json()
        results = response.get("results", [])
        print(f"🔍 {category.title()} → Found {len(results)} in {location}")

        for result in results:
            fsq_id = result.get("fsq_id", "")
            tips = get_tips_for_place(fsq_id)

            for filename, keywords in DIET_FILTERS.items():
                if any(k in tip for tip in tips for k in keywords):
                    venue = {
                        "name": result.get("name", ""),
                        "description": result.get("categories", [{}])[0].get("name", ""),
                        "category": "Foursquare",
                        "location": result.get("location", {}).get("formatted_address", ""),
                        "rating": "",  # Foursquare Basic API doesn't include rating
                        "target_csv": filename
                    }
                    all_results.append(venue)
                    break  # avoid writing the same venue to multiple CSVs

    return all_results
    