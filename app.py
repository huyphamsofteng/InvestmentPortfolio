from flask import Flask
from flask import render_template
from flask import request
from flask import abort, redirect, url_for
from helper import *

app = Flask(__name__)
stocks = []
stock = {
    "symbol": "symbol",
    "shares": "shares",
    "book_value": "book_value",
    "market_price": "market_price"
}
@app.route("/", methods=['POST', 'GET'])
def index():
    stocks = [
        {
        "symbol": "VOO",
        "shares": "10",
        "book_value": "350",
        "market_price": "456"
        },
        {
        "symbol": "APPL",
        "shares": "5",
        "book_value": "375",
        "market_price": "478"
        }
    ]
    return render_template('index.html', stocks = stocks),200

@app.route("/buy", methods=['POST', 'GET'])
def buy():
    if request.method == 'POST':
        symbol = request.form['symbol']
        if(check(symbol)):
            stock["price"] = get_price(symbol)
            stock["symbol"] = symbol
            stocks.append(stock)
            return redirect(url_for('index.html'))
        else:
            return render_template('error.html'), 404
    else:    
        return render_template('buy.html'),200

@app.route("/sell", methods=['POST', 'GET'])
def sell():
    return render_template('sell.html'),200

@app.route("/error")
def error():
    return render_template('error.html'),404


