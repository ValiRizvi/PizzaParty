import requests
from utils.firestore_client import addCouponsToDB

def scrapePapaJohns(storeId: int):

    url = f'https://www.papajohns.com/api/v6/stores/{storeId}/deals'
    
    response = requests.get(url)

    json_response = response.json()
    data = json_response.get('data', {})
    deals = data.get('deals', [])

    # make list of dictionaries
    coupons = []

    for index, deal in enumerate(deals):
        coupon = {}
        coupon['code'] = index + 1
        coupon['description'] = deal.get('description', '')
        coupon['price'] = deal.get('displayPrice', '')

        coupons.append(coupon)

    addCouponsToDB('PapaJohns', str(storeId), coupons)
        


def getPapaJohnsStoreID(postal_code: str):
    url = f'https://www.papajohns.com/order/storesSearchJson?searchType=CARRYOUT&zipcode={postal_code}'

    response = requests.get(url)

    if response.status_code == 200:

        stores = response.json().get('stores', {})

        try: 
            storeId = stores[0].get('storeId')
            return storeId
        
        except:
            # if api return empty array (no stores in proximity)   
            return "Error: No Papa John's locations in proximity."
        
    else:
        print(f'Failed to scrape papa johns: {response.status_code}')
        print(response.text)

        return 'error'