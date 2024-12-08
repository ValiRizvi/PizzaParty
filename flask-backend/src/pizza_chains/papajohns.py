import requests, json
from firestore_client import addCouponToDB

def scrapePapaJohns(postal_code: str):

    url = f'https://www.papajohns.com/order/storesSearchJson?searchType=CARRYOUT&zipcode={postal_code}'

    response = requests.get(url)

    if response.status_code == 200:

        stores = response.json().get('stores', {})

        try: 
            storeId = stores[0].get('storeId')

            url = f'https://www.papajohns.com/api/v6/stores/{storeId}/deals'
            
            response = requests.get(url)

            json_response = response.json()
            data = json_response.get('data', {})
            deals = data.get('deals', [])

            # make list of dictionaries
            coupons = []

            for deal in deals:
                coupon = {}
                coupon['description'] = deal.get('description', '')
                coupon['price'] = deal.get('displayPrice', '')

                coupons.append(coupon)

            addCouponToDB('PapaJohns', coupons)

        # if api return empty array (no stores in proximity)        
        except:
            return "Error: No Papa John's locations in proximity."
        
    else:
        print(f'Failed to scrape papa johns coupons: {response.status_code}')
        print(response.text)


