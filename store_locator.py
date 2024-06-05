import os, json, requests
import googlemaps

api_key = os.environ.get('GOOGLE_MAPS_API_KEY')

gmaps = googlemaps.Client(key=api_key)

postal_code = 'L5M0V7'

geocode_response = gmaps.geocode(postal_code)

location = geocode_response[0]['geometry']['location']
latitude = location['lat']
longitude = location['lng']


url = f'https://order.dominos.ca/store-locator-international/locate/store?regionCode=CA&latitude={latitude}&longitude={longitude}'

response = requests.get(url, headers={'DPZ-Market': 'CANADA'})


stores = response.json().get('Stores', {})
store_number = stores[0].get('StoreID')


data = json.dumps(response.json(), indent=4)

with open('dominos_locations.json', 'w') as file:
    file.write(data)


