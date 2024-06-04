import os 
import googlemaps

api_key = os.environ.get('GOOGLE_MAPS_API_KEY')

gmaps = googlemaps.Client(key=api_key)

postal_code = 'L5M0V7'

geocode_response = gmaps.geocode(postal_code)

location = geocode_response[0]['geometry']['location']
latitude = location['lat']
longitude = location['lng']
print('Latitude:', latitude)
print('Longitude:', longitude)
