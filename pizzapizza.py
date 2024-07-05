import os, requests, json 

def scrapePizzaPizza(store_id):
    url = f'https://www.pizzapizza.ca/ajax/catalog/api/v1/product_list/{store_id}/pickup?category_id=11035'

    headers = {
        "x-request-id": "a58653bf-0e8e-419b-b2f9-090692a51de5",
        "session-token": os.getenv('PIZZAPIZZA_SESSION_TOKEN')
    }

    response = requests.get(url, headers=headers)

    # grab list of coupons from json response
    data = response.json().get('products', [])

    coupons = []

    # loop through list of dictionaries (each dictionary is a coupon/product)
    for product in data: 
        coupon = {}
        coupon['description'] = product.get('description', '')
        coupon['price'] = product.get('price_text', '').get('price_value', '')

        coupons.append(coupon)

    readable_json = json.dumps(coupons, indent=4)

    with open('json_files/pizzapizza_coupons.json', 'w') as file:
        file.write(readable_json)

