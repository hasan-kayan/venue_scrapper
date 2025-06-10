import csv
import os

def write_venue(filename, venue):
    path = f"data/{filename}"
    file_exists = os.path.isfile(path)
    fieldnames = ["name", "description", "category", "location", "rating"]

    with open(path, mode="a", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({key: venue.get(key, "") for key in fieldnames})
