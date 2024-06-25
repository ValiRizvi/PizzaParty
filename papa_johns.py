import requests

def getPapaJohnsStoreID(postal_code):

    url = f'https://www.papajohns.com/order/storesSearchJson?searchType=CARRYOUT&zipcode={postal_code}'

    response = requests.get(url)

    stores = response.json().get('stores', {})
    storeId = stores[0].get('storeId')

    return storeId


