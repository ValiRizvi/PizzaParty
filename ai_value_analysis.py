import os, json, openai, re
from openai import OpenAI

openai.api_key = os.getenv('OPENAI_API_KEY')

def chooseCoupon(number, size):
    # load json
    with open('json_files/dominos_coupons.json', 'r') as file:
        coupons = json.load(file)

    # filter coupons by size to not send extra data to api
    filtered = []

    for coupon in coupons:
        if f'{number} {size}' in coupon['description'] or '%' in coupon['description'] or 'Any Crust' in coupon['description']:
            filtered.append(coupon)
            
        if int(number) >= 2 and size == 'Medium':
            if 'Any 2' in coupon['description']:
                filtered.append(coupon)
        
    # convert to json formatted string to pass to prompt
    coupons_str = json.dumps(filtered)

    prompt = f"Best code for {number} {size} pizza(s). If carryout, next best non-carryout code on next line. Codes only, no text. Prioritize cheapest price. \n{coupons_str}"

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

    return best_value_coupon.split('\n')




