from apis.google_places import search_places_google
from apis.foursquare_places import search_places_foursquare
from utils.csv_writer import write_venue

def run():
    locations = ["New York, USA", "Los Angeles, USA"]
    for location in locations:
        print(f"📍 Searching venues in {location}")
        venues = search_places_google(location) + search_places_foursquare(location)

        for venue in venues:
            print(f"✅ Writing {venue['name']} to {venue['target_csv']}")
            write_venue(venue["target_csv"], venue)

if __name__ == "__main__":
    run()
