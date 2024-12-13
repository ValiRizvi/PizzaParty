from flask import Flask, jsonify, request, json
from flask_cors import CORS

from utils.scrape_stores import scrapeStores
from utils.firestore_client import pullFromDB
from utils.firestore_client import getCouponFromFirestore
from best_value import bestValue


app = Flask(__name__)
CORS(app)


@app.route('/process_postal_code', methods=['POST'])

def processPostalCode():
    # validate user location and collect data to offer relevant services (pizza deals ^.^ )
    postalCode = request.json.get('postalCode')

    if not postalCode:
        return jsonify({'valid': False, 'error': 'Postal code not received.'}), 400

    local_stores = scrapeStores(postalCode)

    # TEST PURPOSES

    allCoupons = {}

    for key, value in local_stores.items():

        coupons = pullFromDB(key, value)
        allCoupons[key] = coupons


    readable_json = json.dumps(allCoupons, indent=4)

    with open(f'flask-backend/src/pizza_chains/json_files/coupons.json', 'w') as file:
        file.write(readable_json)


    bestCouponInfo = bestValue(local_stores, allCoupons)

    bestCoupon = getCouponFromFirestore(bestCouponInfo)

    print(bestCoupon)

    ###############

    # if local stores dict is empty no stores were found 
    if not local_stores:
        return jsonify({'valid': False, 'error': 'There are no stores nearby. Double check your postal code.'}), 200
    
    return jsonify({'valid': True, 'message': 'Pizza has been located. :)'}), 200


if __name__ == '__main__':
    app.run(debug=True)
