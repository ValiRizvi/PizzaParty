from flask import Flask, jsonify, request, render_template, redirect, url_for
import requests

app = Flask(__name__)

@app.route('/')

def home():
    error = request.args.get('error')
    return render_template('index.html', error=error)


@app.route('/submit', methods=['GET'])

def submit():
    number = request.args.get('number')
    size = request.args.get('size')

    if not number or  not size:
        error = 'Please select both a number and size for the pizza(s).'
        return redirect(url_for('home', error=error))

    with open('user_input.txt', 'w') as file:
        file.write(number + '\n')
        file.write(size)

    return f"number: {number} size: {size}"


@app.route('/scrape', methods=['GET'])

def scrape():
    url = request.json.get('url')
    response = requests.get(url)

    return jsonify(response.json())


if __name__ == '__main__':
    app.run(debug=True)
