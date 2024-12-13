import re

# function to condense coupons to essential information only (code, size, number, price)
def condenseCoupons(coupons: list, chain_name: str):

    condensed = []

    for coupon in coupons:
        processed = condense(coupon, chain_name)

        if processed:
            condensed.append(processed)

    return condensed



def condense(coupon: dict, chain_name: str):

    sizes = ['Small', 'Medium', 'Large', 'X-Large', 'Extra-Large', 'XL']

    if chain_name == 'PapaJohns' or chain_name == 'PizzaPizza':
        pizzaPattern = r'(?i)(\b\d+\b|\b(one|two|three|four)\b)?\s*(Small|Medium|Large|XL|Extra\s*-?\s*Large)\b'
    elif chain_name == 'Dominos':
        pizzaPattern = r'(?i)(\b\d+\b)?\s*(X-Large|Large|Medium|Small)\b'
    else:
        return []

    if not coupon.get('price'):
        return None

    description = coupon.get('description', '')
    matches = re.finditer(pizzaPattern, description) # search description for matches with appropriate regex pattern

    # default values for number and size
    number = 1
    size = ''

    for match in matches:

        if chain_name == 'PapaJohns' or chain_name == 'PizzaPizza':
                # check for number match (word or integer)
            if match.group(1):
                # If word number matched convert to integer
                if match.group(2):
                    number = wordNumToInt(match.group(2))
                else:
                    number = int(match.group(1))
            
            size = match.group(3).title()

        elif chain_name == 'Dominos':
            size_match = match.group(2).title()  
            number_match = match.group(1)     

            # update the size and number only if it's the largest size match in the description
            if size == '' or sizes.index(size_match) > sizes.index(size):
                size = size_match

                if number_match: 
                    number = int(number_match)

    # edge case for descriptions that have 'pizza' but no size specified -- default to medium 
    isPizza = 'pizza' in description.lower()

    # skip coupon if no size matches
    if not size:
        if not isPizza:
            return None
        else:
            size = 'Medium'


    return {
        'code': coupon.get('code'),  
        'price': coupon.get('price'),
        'number': number,
        'size': size
    }


# convert written numbers to integers
def wordNumToInt(word: str):

    wordNums = {'one': 1, 'two': 2, 'three': 3, 'four': 4}

    return wordNums.get(word.lower(), 1)  # default to 1 if no match
