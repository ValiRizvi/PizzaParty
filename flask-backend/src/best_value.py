from utils.coupon_condenser import condenseCoupons
from utils.surface_area import getTotalSurfaceArea

def bestValue(local_stores: dict, allCoupons: dict):
    
    # create dictionary of condensed coupons of only the available stores
    condensed = {}

    for chain_name in local_stores.keys():

        coupons = allCoupons.get(chain_name, [])

        if coupons:
            processed = condenseCoupons(coupons, chain_name)
            if processed:
                condensed[chain_name] = processed
        
    
    # calculate surface area of pizza provided by each coupon, add result as a coupon key-value pair

    bestValue = {
        'storeId': '',
        'chain': '',
        'code': '',
        'value': 0.0
    }

    for key in condensed.keys():
        for coupon in condensed[key]:
            size = coupon.get('size')
            number = coupon.get('number')
            price = coupon.get('price')

            surfaceArea = getTotalSurfaceArea(size, number)
            value = surfaceArea / price
            
            if value > bestValue['value']:
                bestValue['chain'] = key
                bestValue['code'] = coupon.get('code')
                bestValue['value'] = value

    
    bestValue['storeId'] = local_stores[bestValue['chain']]
    
    return bestValue




    