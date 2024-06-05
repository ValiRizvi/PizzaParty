import requests
import json

app_url = 'http://127.0.0.1:5000/scrape'

store_number = 10285

api_url = f'https://order.dominos.ca/power/store/{store_number}/menu?lang=en&structured=true'


# send request to flask scrape endpoint with the url to scrape as the json payload
payload = {'url': api_url}
response = requests.post(app_url, json=payload)


if response.status_code == 200:
    print(response.status_code)

    data = response.json()
    coupons_data = data.get('Coupons', {})

    # make list of dictionaries
    coupons = []

    # loop through 
    for key, value in coupons_data.items():
        coupon = {
            'code': value.get('Code', ''),
            'description': value.get('Name', ''),
            'price': value.get('Price', '')
        }
        coupons.append(coupon)

    # convert python dictionary to json for readability
    readable_json = json.dumps(coupons, indent=4)

    # write readable json to txt file
    with open('dominos.json', 'w') as file:
        file.write(readable_json)
    
else:
    print(f'Failed to retrieve data: {response.status_code}')
    print(response.text)
