import re
import pandas as pd

with open('data.txt') as file:
    data = file.read()

# regex object (chatgpt created filter)
filter = re.compile(r'ADD COUPON\s+\$(\d+\.\d+)\s+(.+?)\s+\(CODE: (\w+)\)', re.DOTALL)

# store data in tuples in format (price, description, code)
sets = filter.findall(data)

# convert tuples into list of dictionaries
coupons = []
for coupon in sets:
    price, description, code = coupon
    coupons.append({
        'Price': price,
        'Description': description.strip().replace('\n', ' '),
        'Code': code
    })

# convert to pandas dataframe for readability
df = pd.DataFrame(coupons)
print(df)