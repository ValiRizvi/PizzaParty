import requests
from utils.firestore_client import addCouponsToDB


def scrapeDominos(store_number: int):
    api_url = f'https://order.dominos.ca/power/store/{store_number}/menu?lang=en&structured=true'

    response = requests.get(api_url)

    if response.status_code == 200:
        print(response.status_code)

        data = response.json()
        coupons_data = data.get('Coupons', {})

        # make list of dictionaries
        coupons = []

        # loop through 
        for value in coupons_data.values():
            coupon = {
                'code': value.get('Code', ''),
                'description': value.get('Name', ''),
                'price': value.get('Price', '')
            }
            coupons.append(coupon)

        addCouponsToDB('Dominos', str(store_number), coupons)
        
    else:
        print(f'Failed to scrape dominos coupons: {response.status_code}')
        print(response.text)



def getDominosStoreID(coordinates: dict):

    # use lat and long to complete url and request json listing closest dominos stores
    url = f'https://order.dominos.ca/store-locator-international/locate/store?regionCode=CA&latitude={coordinates['latitude']}&longitude={coordinates['longitude']}'

    response = requests.get(url, headers={'DPZ-Market': 'CANADA'})

    if response.status_code == 200:
        # store and return closest Dominos store ID
        stores = response.json().get('Stores', {})

        try: 
            store_number = stores[0].get('StoreID', '')
        except:
            # if there are no store id's in the json (no stores in relative proximity)
            return "Error: No Domino's locations in proximity."

        # type casting to int to match logic in scrape_stores.py
        return int(store_number)
    
    else:
        print(f'Failed to retrieve dominos store id: {response.status_code}')
        print(response.text)

        return 'error'