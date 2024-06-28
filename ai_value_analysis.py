import os, json, openai
from openai import OpenAI
from filter_coupons import filterDominosCoupons

openai.api_key = os.getenv('OPENAI_API_KEY')

def chooseCoupon(number, size):
    
    filtered = filterDominosCoupons(number, size)
        
    # convert to json formatted string to pass to prompt
    coupons_str = json.dumps(filtered)

    prompt = f'Best code for {number} {size} pizza(s). If carryout, next best non-carryout code on next line. Codes only, no text. Prioritize lowest price. \n{coupons_str}'

    # make api request
    client = OpenAI()

    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt}
        ],
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0
    )

    # extract list of codes
    best_value_coupon = completion.choices[0].message.content

    return best_value_coupon.split('\n')




