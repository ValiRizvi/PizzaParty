import requests, json

def getPapaJohnsStoreID(postal_code):

    url = f'https://www.papajohns.com/order/storesSearchJson?searchType=CARRYOUT&zipcode={postal_code}'

    response = requests.get(url)

    stores = response.json().get('stores', {})
    storeId = stores[0].get('storeId')

    return storeId


def getDeals(storeId):

    url = f'https://www.papajohns.com/api/v6/stores/{storeId}/deals'
    
    response = requests.get(url)
    
    data = response.json()
    deals = data.get('deals', {})

    # make list of dictionaries
    coupons = []

    # loop through 
    for key, value in deals.items():
        coupon = {
            'description': value.get('description', ''),
            'price': value.get('displayPrice', '')
        }
        coupons.append(coupon)

    # convert python dictionary to json for readability
    readable_json = json.dumps(coupons, indent=4)

    return readable_json

print(getDeals(getPapaJohnsStoreID))
