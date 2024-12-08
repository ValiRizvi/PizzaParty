import os, googlemaps

api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
gmaps = googlemaps.Client(key=api_key)


def getCoordinates(postal_code: str):

    # get lat and long of given postal code
    geocode_response = gmaps.geocode(postal_code)

    location = geocode_response[0]['geometry']['location']

    coordinates = {}
    coordinates['latitude'] = location['lat']
    coordinates['longitude'] = location['lng']

    return coordinates





