import os, requests, json 
from firestore_client import addCouponToDB

def scrapePizzaPizza(store_id: str):
    url = f'https://www.pizzapizza.ca/ajax/catalog/api/v1/product_list/{store_id}/pickup?category_id=11035'

    headers = {
        "x-request-id": "a58653bf-0e8e-419b-b2f9-090692a51de5",
        "session-token": os.getenv('PIZZAPIZZA_SESSION_TOKEN')
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # grab list of coupons from json response
        data = response.json().get('products', [])

        coupons = []

        # loop through list of dictionaries (each dictionary is a coupon/product)
        for product in data: 
            coupon = {}
            coupon['description'] = product.get('description', '')
            coupon['price'] = product.get('price_text', '').get('price_value', '')

            coupons.append(coupon)

        addCouponToDB('PizzaPizza', coupons)

    else:
        print(f'Failed to scrape pizzapizza coupons: {response.status_code}')
        print(response.text)


def getPizzaPizzaStoreID(coordinates: dict):

    url = f'https://www.pizzapizza.ca/ajax/store/api/v1/search/?latitude={coordinates['latitude']}&longitude={coordinates['longitude']}'

    headers = {
        "x-request-id": "a58653bf-0e8e-419b-b2f9-090692a51de5",
        "session-token": os.getenv('PIZZAPIZZA_SESSION_TOKEN')
    }   

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        stores = response.json().get('stores', {})

        try:
            store_id = stores[0].get('store_id', '')
        except: 
            # if there are no store id's in the json (no stores in relative proximity)
            return "Error: No Pizza Pizza locations in proximity."

        return store_id
    
    else:
        print(f'Failed to retrieve pizzapizza store id: {response.status_code}')
        print(response.text)
