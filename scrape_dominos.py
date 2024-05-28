import requests
import json

app_url = 'http://127.0.0.1:5000/scrape'

store_number = 10285

api_url = f'https://order.dominos.ca/power/store/{store_number}/menu?lang=en&structured=true'

response = requests.get(api_url)

if response.status_code == 200:
    print(response.status_code)
    data = response.json()
    readable_json = json.dumps(data, indent=4)

    with open('dominos_coupons.txt', 'w') as file:
        file.write(readable_json)
    
else:
    print(f"Failed to retrieve data: {response.status_code}")
    print(response.text)
