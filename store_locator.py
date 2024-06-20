import os, requests
import googlemaps

api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
gmaps = googlemaps.Client(key=api_key)


def getStoreID(postal_code):

    # get lat and long of given postal code
    geocode_response = gmaps.geocode(postal_code)

    location = geocode_response[0]['geometry']['location']
    latitude = location['lat']
    longitude = location['lng']

    # use lat and long to complete url and request json listing closest dominos stores
    url = f'https://order.dominos.ca/store-locator-international/locate/store?regionCode=CA&latitude={latitude}&longitude={longitude}'

    response = requests.get(url, headers={'DPZ-Market': 'CANADA'})

    # store and return closest Dominos store ID
    stores = response.json().get('Stores', {})
    store_number = stores[0].get('StoreID')

    return store_number




