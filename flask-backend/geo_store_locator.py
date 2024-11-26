import os, requests
import googlemaps

api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
gmaps = googlemaps.Client(key=api_key)

def getCoordinates(postal_code):
    # get lat and long of given postal code
    geocode_response = gmaps.geocode(postal_code)

    location = geocode_response[0]['geometry']['location']

    coordinates = {}
    coordinates['latitude'] = location['lat']
    coordinates['longitude'] = location['lng']

    return coordinates


def getDominosStoreID(postal_code):

    coordinates = getCoordinates(postal_code)

    # use lat and long to complete url and request json listing closest dominos stores
    url = f'https://order.dominos.ca/store-locator-international/locate/store?regionCode=CA&latitude={coordinates['latitude']}&longitude={coordinates['longitude']}'

    response = requests.get(url, headers={'DPZ-Market': 'CANADA'})

    # store and return closest Dominos store ID
    stores = response.json().get('Stores', {})
    store_number = stores[0].get('StoreID', '')

    return store_number


def getPizzaPizzaStoreID(postal_code):

    coordinates = getCoordinates(postal_code)

    url = f'https://www.pizzapizza.ca/ajax/store/api/v1/search/?latitude={coordinates['latitude']}&longitude={coordinates['longitude']}'

    headers = {
        "x-request-id": "a58653bf-0e8e-419b-b2f9-090692a51de5",
        "session-token": os.getenv('PIZZAPIZZA_SESSION_TOKEN')
    }   

    response = requests.get(url, headers=headers)

    stores = response.json().get('stores', {})
    store_id = stores[0].get('store_id', '')

    return store_id




