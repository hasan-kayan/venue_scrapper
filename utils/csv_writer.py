import csv
import os

def write_venue(filename, venue):
    path = f"data/{filename}"
    file_exists = os.path.isfile(path)
    with open(path, mode="a", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "description", "category", "location", "rating"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(venue)
