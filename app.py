from flask import Flask
from flask import render_template
from flask import request
from flask import abort, redirect, url_for
from helper import *

app = Flask(__name__)
stocks = [
    {
    "symbol": "VOO",
    "shares": "10",
    "book_value": "book_value",
    "price": "456"
},
{
    "symbol": "APPL",
    "shares": "5",
    "book_value": "book_value",
    "price": "478"
}
]
stock = {
    "symbol": "symbol",
    "shares": "shares",
    "book_value": "book_value",
    "price": "price"
}
@app.route("/", methods=['POST', 'GET'])
def index():
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


