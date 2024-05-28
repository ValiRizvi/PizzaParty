from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/')

def test():
    return 'test'


@app.route('/scrape', methods=['POST'])

def scrape():
    url = request.json.get('url')
    response = requests.get(url)
    data = response.json()

    return jsonify({'data':data})


if __name__ == '__main__':
    app.run(debug=True)
