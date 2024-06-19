from flask import Flask, jsonify, request, render_template, redirect, url_for
import requests
from store_locator import getStoreID
from scrape_dominos import scrapeDominos
from ai_value_analysis import chooseCoupon

app = Flask(__name__)

@app.route('/')

def home():
    error = request.args.get('error')
    return render_template('index.html', error=error)


@app.route('/submit', methods=['GET'])

def submit():
    number = request.args.get('number')
    print(type(number))
    size = request.args.get('size')
    postalCode = request.args.get('postalCode')

    store_number = getStoreID(postalCode)
    print(store_number)
    scrapeDominos(store_number)

    if not number or not size:
        error = 'Please select both a number and size for the pizza(s).'
        return redirect(url_for('home', error=error))

    with open('user_input.txt', 'w') as file:
        file.write(number + '\n')
        file.write(size + '\n')

    best_coupons = chooseCoupon(number, size)

    return f'number: {number}, size: {size} \n Best Coupons: {best_coupons}'


@app.route('/scrape', methods=['POST'])

def scrape():
    url = request.json.get('url')
    response = requests.get(url)

    return jsonify(response.json())


if __name__ == '__main__':
    app.run(debug=True)
