import requests

app_url = 'http://127.0.0.1:5000/scrape'

website_to_scrape = 'https://www.dominos.ca/'

# json payload to send
data = {'url': website_to_scrape}

# send POST request to /scrape endpoint
response = requests.post(app_url, json=data)

print(response.status_code)
print(response.json())
