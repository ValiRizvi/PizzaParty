from flask import Flask, jsonify, request
from flask_cors import CORS

from utils.scrape_stores import scrapeStores


app = Flask(__name__)
CORS(app)


@app.route('/validate_postal_code', methods=['POST'])

def validatePostalCode():
    postalCode = request.json.get('postalCode')

    if not postalCode:
        return jsonify({'valid': False, 'error': 'Postal code not received.'}), 400

    found = scrapeStores(postalCode)
    if not found:
        return jsonify({'valid': False, 'error': 'There are no stores nearby. Double check your postal code.'}), 200
    
    return jsonify({'valid': True, 'message': 'Pizza has been located. :)'}), 200


if __name__ == '__main__':
    app.run(debug=True)
