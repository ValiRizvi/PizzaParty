import os, json, openai
from openai import OpenAI

openai.api_key = os.getenv('OPENAI_API_KEY')

# load json
with open('json_files/dominos_coupons.json', 'r') as file:
    coupons = json.load(file)

# save user inputs to variables to pass to prompt
with open('user_input.txt', 'r') as file:
    number = file.readline().strip()
    size = file.readline().strip()

# filter coupons by size to not send extra data to api
def filter_coupons_by_size(coupons, size):
    filtered = []

    for coupon in coupons:
        if size in coupon['description'] or '%' in coupon['description']:
            filtered.append(coupon)
    
    return filtered

# convert to json formatted string to pass to prompt
coupons_str = json.dumps(filter_coupons_by_size(coupons, size))

prompt = f"Best code for 2 medium pizza(s) {coupons_str}. If carryout, next best non-carryout code on next line. Codes only, no text."


client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=5,
    n=1,
    stop=None,
    temperature=0
)

best_value_coupon = completion.choices[0].message.content

print(best_value_coupon)

