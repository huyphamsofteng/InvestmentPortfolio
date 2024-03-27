from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect, url_for
from helper import *

app = Flask(__name__)
app.secret_key = b'_5#y2L"F6868\n\abc]/'
create_db()
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username'].upper()
        password = request.form['password']
        if get_login_username(username) == None:
            error_m = "Username not Found!"
            return render_template('error.html',error_m = error_m),404
        else:
            if not check_password(username,password):
                error_m = "Password not correct!"
                return render_template('error.html',error_m = error_m),404
            else:
                session["username"] = username
                s = "in"
                return redirect("/")
    else:
        return render_template("login.html"),200

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].upper()
        password = request.form['password']
        if get_login_username(username):
            error_m = "Username already exist!"
            return render_template('error.html',error_m = error_m),404
        else:
            generate_user(username, password)
            session["username"] = username
            s = "in"
            return redirect("/")
    else:
        return render_template("signup.html"),200
     
@app.route('/logout')
def logout():
    session.pop('username', None)
    s = None
    return redirect(url_for("login", s = s))

@app.route("/", methods=['POST', 'GET'])
def index():
    if 'username' in session:
        db_check = check_db()
        stocks = []
        if(not db_check):
            error_m = "Cannot connect to Database. Please try again."
            return render_template('error.html',error_m = error_m),404
        user = get_user(session["username"])
        stocks = get_all_stocks(user["user_id"])
        bv = 0 
        mv = 0
        for stock in stocks:
            bv = bv + stock["book_value"]
            mv = mv + stock["market_value"]
        if (mv == 0):
            gain_loss = 0
        else:
            gain_loss = (mv-bv) / bv * 100
            gain_loss = round(gain_loss, 2)
        s = "in"
        return render_template('index.html', stocks = stocks, s = s, total_value = user["total_value"], gain_loss = gain_loss),200
    else:
        s = None
        return render_template("login.html", s = s),200

@app.route("/buy", methods=['POST', 'GET'])
def buy():
    if 'username' in session:
        s = "in"
        if request.method == 'POST':
            symbol = request.form['symbol'].upper()
            shares = int(request.form['shares'])   
            user = get_user(session["username"])
            if(get_price(symbol)): 
                stocks = get_all_stocks(user["user_id"])
                check_buy = True
                total_value = user["total_value"]
                for stock in stocks:
                    if stock["symbol"] == symbol:
                        market_value = get_price(symbol)
                        book_value = stock["book_value"] + market_value * shares
                        shares = stock["shares"] + shares
                        if (total_value - book_value) < 0:
                            error_m = "Not enough money!"
                            return render_template('error.html',error_m = error_m, s = s ),404
                        total_value = total_value - book_value
                        cursor.execute(f"UPDATE stock SET book_value = {book_value}, shares = {shares} WHERE symbol = '{symbol}' AND user_id = {user["user_id"]}")
                        check_buy = False
                if check_buy == True:
                    book_value = get_price(symbol) * shares
                    book_value = round(book_value, 2)
                    total_value = total_value - book_value
                    cursor.execute(f"INSERT INTO stock (symbol, book_value, shares, user_id) VALUES ('{symbol}',{book_value},{shares},{user["user_id"]})")
                cursor.execute(f"UPDATE user SET total_value = {total_value}")
                cnx.commit()
                return redirect(url_for('index'))
            else:
                error_m = "Symbol Not Found!"
                return render_template('error.html',error_m = error_m, s = s ),404
        else:    
            return render_template('buy.html', s = s),200
    else:
        s = None
        return redirect(url_for("login", s = s))

@app.route("/sell", methods=['POST', 'GET'])
def sell():
    if 'username' in session:
        s = "in"    
        if request.method == 'POST':
            symbol = request.form['symbol'].upper()
            shares = int(request.form['shares'])   
            user = get_user(session["username"])
            cursor.execute(f"SELECT * FROM stock WHERE user_id = {user["user_id"]} AND symbol = '{symbol}'")
            temp = cursor.fetchone()
            if temp[3] < shares:
                error_m = "Shares are not enough!"
                return render_template('error.html',error_m = error_m),404
            total_value = user['total_value'] + temp[3] * get_price(symbol)
            book_value = temp[2] - temp[2] / temp[3] * shares
            shares = temp[3] - shares
            cursor.execute(f"UPDATE user SET total_value = {total_value} WHERE user_id = {user["user_id"]}")
            cursor.execute(f"UPDATE stock SET book_value = {book_value}, shares = {shares} WHERE symbol = '{symbol}' AND user_id = {user["user_id"]}")
            delete_zero_stock(user["user_id"])
            cnx.commit()
            return redirect(url_for('index'))
        else:
            stocks = []
            user = get_user(session["username"])
            stocks = get_all_stocks(user["user_id"])
            return render_template('sell.html', stocks = stocks, s = s),200
    else:
        s = None
        return redirect(url_for("login", s = s))

@app.route("/error")
def error():
    if 'username' in session:
        s = 'in'
        return render_template('error.html',s = s),404
    else:
        error_m = "Please Log In"
        return render_template('error.html',error_m = error_m),404


