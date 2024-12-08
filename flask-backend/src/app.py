from flask import Flask, jsonify, request, render_template, redirect, url_for
import requests
from flask_cors import CORS

from utils.scrape_stores import scrapeStores


app = Flask(__name__)
CORS(app)

@app.route('/')

def home():
    error = request.args.get('error')
    return render_template('index.html', error=error)



@app.route('/validate_postal_code', methods=['POST'])

def validatePostalCode():
    postalCode = request.json.get('postalCode')

    if not postalCode:
        return jsonify({'valid': False, 'error': 'Postal code not received.'}), 400

    found = scrapeStores(postalCode)
    if not found:
        return jsonify({'valid': False, 'error': 'There are no stores nearby. Double check your postal code.'}), 200
    
    return jsonify({'valid': True, 'message': 'Pizza has been located. :)'}), 200



@app.route('/scrape', methods=['POST'])

def scrape():
    url = request.json.get('url')
    response = requests.get(url)

    return jsonify(response.json())



if __name__ == '__main__':
    app.run(debug=True)
