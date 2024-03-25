from flask import Flask
from flask import render_template
from flask import request
from flask import abort, redirect, url_for
from helper import *

app = Flask(__name__)
user = {
    "user_id": 1,
    "user_name": "admin",
    "user_password": "password",
    "total_value": 10000
}
@app.route("/", methods=['POST', 'GET'])
def index():
    db_check = check_db()
    stocks = []
    if( not db_check):
       error_m = "Cannot connect to Database. Please try again."
       return render_template('error.html',error_m = error_m),404
    cnx = mysql.connector.connect(user='dpham', password='0918', host='127.0.0.1', database='stockbase')
    cursor = cnx.cursor()
    user_id = 1
    stocks = get_all_stocks(user_id)
    return render_template('index.html', stocks = stocks),200

@app.route("/buy", methods=['POST', 'GET'])
def buy():
    if request.method == 'POST':
        symbol = request.form['symbol'].upper()
        shares = int(request.form['shares'])   
        user_id = 1   
        check_buy = True
        stocks = get_all_stocks(user_id)
        check_api = check(symbol) 
        if(check_api):
            if check_api == 429:
                error_m = "Too Many Request! Please Try Again Tomorrow!"
                return render_template('error.html',error_m = error_m),404
            for stock in stocks:
                if stock["symbol"] == symbol:
                    market_value = get_price(symbol)
                    book_value = stock["book_value"] + market_value * shares
                    shares = stock["shares"] + shares
                    total_value = user["total_value"] - book_value
                    cursor.execute(f"UPDATE stock SET book_value = {book_value}, shares = {shares} WHERE symbol = '{symbol}'")
                    cursor.execute(f"UPDATE user SET total_value = {total_value}")
                    cnx.commit()
                    check_buy = False
            if check_buy == True:
                book_value = get_price(symbol) * shares
                book_value = round(book_value, 2)
                cursor.execute(f"INSERT INTO stock (symbol, book_value, shares, user_id) VALUES ('{symbol}',{book_value},{shares},{user_id})")
                cnx.commit()
            return redirect(url_for('index'))
        else:
            error_m = "Symbol Not Found!"
            return render_template('error.html',error_m = error_m),404
    else:    
        return render_template('buy.html'),200

@app.route("/sell", methods=['POST', 'GET'])
def sell():
    if request.method == 'POST':
        symbol = request.form['symbol'].upper()
        shares = int(request.form['shares'])   
        user_id = 1
        cursor.execute(f"SELECT * FROM stock WHERE user_id = {user_id} AND symbol = '{symbol}'")
        temp = cursor.fetchone()
        if temp[2] < shares:
            error_m = "Shares are not enough!"
            return render_template('error.html',error_m = error_m),404
        total_value = user['total_value'] + temp[2] * get_price(symbol)
        book_value = temp[1] - temp[1] / temp[2] * shares
        shares = temp[2] - shares
        cursor.execute(f"UPDATE user SET total_value = {total_value}")
        cursor.execute(f"UPDATE stock SET book_value = {book_value}, shares = {shares} WHERE symbol = '{symbol}'")
        cnx.commit()
        return redirect(url_for('index'))
    else:
        user_id = 1
        stocks = []
        stocks = get_all_stocks(user_id)
        return render_template('sell.html', stocks = stocks),200

@app.route("/error")
def error():
    return render_template('error.html'),404


