import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def load_filters():
    with open("config/filters.json", "r", encoding="utf-8") as f:
        return json.load(f)

DIET_FILTERS = load_filters()

def get_place_details(place_id, venue_name):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "review",
        "key": GOOGLE_API_KEY
    }

    response = requests.get(url, params=params).json()
    reviews = response.get("result", {}).get("reviews", [])

    if not reviews:
        print(f"🛑 No reviews found for: {venue_name} ({place_id})")
    else:
        print(f"📝 {len(reviews)} reviews found for: {venue_name}")

    return [review.get("text", "").lower() for review in reviews if "text" in review]
def search_places_google(location):
    search_types = ["restaurant", "cafe", "bar"]
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    all_results = []

    for type_name in search_types:
        params = {
            "query": f"{type_name} in {location}",
            "key": GOOGLE_API_KEY
        }

        response = requests.get(url, params=params).json()
        results = response.get("results", [])
        print(f"🔍 {type_name.title()} → Found {len(results)} in {location}")

        for result in results:
            venue_name = result.get("name", "Unnamed")
            place_id = result.get("place_id", "")
            print(f"\n➡️ Checking venue: {venue_name}")

            comments = get_place_details(place_id, venue_name)

            matched = False
            for filename, keywords in DIET_FILTERS.items():
                for comment in comments:
                    for keyword in keywords:
                        if keyword.lower() in comment:
                            print(f"✅ Match found for '{keyword}' in reviews of {venue_name} → {filename}")
                            venue = {
                                "name": venue_name,
                                "description": " ".join(result.get("types", [])),
                                "category": "Google",
                                "location": result.get("formatted_address", ""),
                                "rating": result.get("rating", ""),
                                "target_csv": filename
                            }
                            all_results.append(venue)
                            matched = True
                            break
                    if matched:
                        break
                if matched:
                    break
            if not matched:
                print(f"❌ No matching keywords found in reviews for: {venue_name}")

    return all_results
