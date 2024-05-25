from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')

def test():
    return 'test'

def scrape():
    url = request.json('url')
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = [p.text for p in soup.find_all('p')]
    
    return jsonify({'data':paragraphs})


if __name__ == '__main__':
    app.run()
