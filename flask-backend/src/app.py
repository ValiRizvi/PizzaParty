from flask import Flask, jsonify, request
from flask_cors import CORS

from utils.scrape_stores import scrapeStores
from utils.firestore_client import pullFromDB, getCouponFromFirestore, storeEmbeddingInDB
from embedding import generateEmbeddings
from best_value import bestValue
from most_similar import mostSimilar

import json



app = Flask(__name__)
CORS(app)


@app.route('/process_postal_code', methods=['POST'])

def processPostalCode():
    # validate user location and collect data to offer relevant services (pizza deals ^.^ )
    postalCode = request.json.get('postalCode')

    if not postalCode:
        return jsonify({'valid': False, 'error': 'Postal code not received.'}), 400


    '''
        local_stores returns a dict of the chains that are available.  key=chain_name : value=store_id

    ex. local_stores = {
            'Dominos': '12345',
            'PapaJohns': '54321'
        }
    '''
    local_stores = scrapeStores(postalCode)

    # TEST PURPOSES #

    allCoupons = {}

    for key, value in local_stores.items():

        coupons = pullFromDB(chain_name=key, store_id=value, collection_to_pull='coupons')
        allCoupons[key] = coupons
        

    ### BEST VALUE COUPON FUNCTION
    bestCouponInfo = bestValue(local_stores, allCoupons)

    bestCoupon = getCouponFromFirestore(bestCouponInfo)

    print(json.dumps(bestCoupon, indent=4))



    ### MOST SIMILAR COUPON FUNCTION
    allCouponsEmbedded = generateEmbeddings(local_stores, allCoupons)

    userInput = '1 Medium Feast Pizza'
    most_similar_coupon = mostSimilar(
        userInput=userInput,
        allCouponsEmbedded=allCouponsEmbedded
    )

    print(json.dumps(most_similar_coupon, indent=4))
    

    ################

    # if local stores dict is empty no stores were found 
    if not local_stores:
        return jsonify({'valid': False, 'error': 'There are no stores nearby. Double check your postal code.'}), 200
    
    return jsonify({'valid': True, 'message': 'Pizza has been located. :)'}), 200


if __name__ == '__main__':
    app.run(debug=True)
