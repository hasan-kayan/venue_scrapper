from apis.google_places import search_places_google
from apis.foursquare_places import search_places_foursquare
from utils.csv_writer import write_venue

def run():
    locations = ["New York, USA", "Los Angeles, USA"]  # or use geocoords
    for location in locations:
        print(f"📍 Searching venues in {location}")
        venues_google = search_places_google(location)
        venues_foursquare = search_places_foursquare(location)
        print(f"🔍 Found {len(venues_google)} from Google, {len(venues_foursquare)} from Foursquare")

        venues = venues_google + venues_foursquare


        for venue in venues:
            name = venue.get("name", "").lower()
            description = venue.get("description", "").lower()
            category = venue.get("category", "").lower()

            text = f"{name} {description} {category}"
            if any(k in text for k in ["gluten free", "gluten-free"]):
                write_venue("gluten_free.csv", venue)
            if any(k in text for k in ["vegan", "vegetarian"]):
                write_venue("vegan_vegetarian.csv", venue)
            if "kosher" in text:
                write_venue("kosher.csv", venue)

if __name__ == "__main__":
    run()
