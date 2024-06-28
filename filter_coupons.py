import json

def filterDominosCoupons(number, size):
    # load json
    with open('json_files/dominos_coupons.json', 'r') as file:
        coupons = json.load(file)

    # filter coupons by size to not send extra data to api
    filtered = []

    for coupon in coupons:
        if f'{number} {size}' in coupon['description'] or '%' in coupon['description'] or 'Any Crust' in coupon['description']:
            filtered.append(coupon)
        
        # dominos 2+ medium $8.99 deal doesnt state the size in the description so this is just to check if that is available
        if int(number) >= 2 and size == 'Medium':
            if 'Any 2' in coupon['description']:
                filtered.append(coupon)

    return filtered