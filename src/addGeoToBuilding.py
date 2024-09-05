import csv
import time
from requests import get
from urllib.parse import quote

buildings = []

# Get your API key from here: https://geocode.maps.co/
api_key = "YOUR GEOCODE API KEY"
if api_key == "YOUR GEOCODE API KEY":
    print("Geocode API required to run.")
    exit()

with open('assets/buildings.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        buildings.append((row[1], row[2]))

buildings = buildings[1:]

with open('assets/buildingsGeo.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for building in buildings:
        encoded_address = quote(building[1])
        query = "https://geocode.maps.co/search?q="+encoded_address+"&api_key=" + api_key
        res = get(query)
        lat = 0
        lon = 0
        if res.status_code == 200:
            resjson = res.json()[0]
            print(resjson)
            lat = float(resjson["lat"])
            lon = float(resjson["lon"])
        else:
            exit()
        writer.writerow([building[0], building[1], lat, lon])
        time.sleep(1.1)