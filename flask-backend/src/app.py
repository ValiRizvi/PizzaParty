from flask import Flask, jsonify, request
from flask_cors import CORS

from utils.scrape_stores import scrapeStores
from utils.firestore_client import pullFromDB, getCouponFromFirestore
from utils.embedding import generateEmbeddings

from main_functions.best_value import bestValue
from main_functions.most_similar import mostSimilar

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

    # if local stores dict is empty no stores were found 
    if not local_stores:
        return jsonify({'valid': False, 'error': 'There are no stores nearby. Double check your postal code.'}), 200
    
    
    allCoupons = {}

    for key, value in local_stores.items():

        coupons = pullFromDB(chain_name=key, store_id=value, collection_to_pull='coupons')
        allCoupons[key] = coupons

    return jsonify({'valid': True, 'local_stores': local_stores, 'allCoupons': allCoupons}), 200
        


@app.route('/best_value', methods=['POST'])

def getBestValue():

    local_stores = request.json.get('local_stores')
    allCoupons = request.json.get('allCoupons')

    bestCouponInfo = bestValue(local_stores, allCoupons)  # dict of info of coupon with highes value rating

    bestCoupon = getCouponFromFirestore(bestCouponInfo)  # use information to pull correct coupon from db

    print(json.dumps(bestCoupon, indent=4))

    return jsonify({ 'coupon': bestCoupon }), 200

    ''' bestCoupon is a dict in the shape:
    {
        'chain': 'Dominos',
        'code': '12345',
        'value': 12.88,
        'store_id': '101',
        'coupon': {
            'price': '7.49',
            'description': ' ... ',       
            'code': '12345'
        }
    }
    '''



@app.route('/most_similar', methods=['POST'])

def findMostSimilar():

    local_stores = request.json.get('local_stores')
    allCoupons = request.json.get('allCoupons')
    userInput = request.json.get('userInput')

    # returns dict of vectors representing coupons for cosine similarity comparison 
    allCouponsEmbedded = generateEmbeddings(local_stores, allCoupons)  

    # returns dict of all info of most similar coupon to user input
    most_similar_coupon = mostSimilar(
        userInput=userInput,
        allCouponsEmbedded=allCouponsEmbedded
    )

    print(json.dumps(most_similar_coupon, indent=4))

    return jsonify({ 'mostSimilar': most_similar_coupon }), 200


if __name__ == '__main__':
    app.run(debug=True)
