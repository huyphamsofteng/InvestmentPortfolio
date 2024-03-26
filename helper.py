import yfinance as yf
import requests
from flask import Flask
import mysql.connector
from flask_bcrypt import Bcrypt
app = Flask(__name__)
bcrypt = Bcrypt(app)

def check_db():
    try:
        cnx = mysql.connector.connect(user='dpham', password='0918', host='127.0.0.1', database='stockbase')
        return True
    except Exception as e:
        return False

cnx = mysql.connector.connect(user='dpham', password='0918', host='127.0.0.1', database='stockbase')
cursor = cnx.cursor(buffered=True)

def create_db():
    cursor.execute("CREATE DATABASE IF NOT EXISTS stockbase")
    cursor.execute("CREATE TABLE IF NOT EXISTS stock (symbol CHAR(4), book_value FLOAT(7), shares INT(100), user_id INT(25), PRIMARY KEY (symbol))")
    cursor.execute("CREATE TABLE IF NOT EXISTS user (user_id INT(100) auto_increment, user_name CHAR(10), user_password LONGTEXT, total_value FLOAT(7) DEFAULT 10000 ,PRIMARY KEY (user_id))")
    cnx.commit()
    
def get_price(symbol):
    call = yf.Ticker(f"{symbol}")
    if 'bid' in call.info.keys():
        return call.info['bid']
    else:
        return None

def get_all_stocks(user_id):
    stocks=[]
    stock={}
    cursor.execute(f"SELECT * FROM stock WHERE user_id = {user_id}")
    temps = cursor.fetchall()
    for temp in temps:
        stock["symbol"] = temp[0].upper()
        stock["book_value"] = round(float(temp[1]),2)
        stock["shares"] = int(temp[2])
        stock["user_id"] = int(temp[3])
        stock["market_value"] = round((stock["shares"] * get_price(stock["symbol"])),2)
        stocks.append(stock.copy())
    return stocks.copy()


def get_login_username(username):
    cursor.execute(f"SELECT user_name FROM user WHERE user_name = '{username}'")
    temp = cursor.fetchone()
    if temp == None:
        return None
    return temp[0]

def check_password(username,password):
    user = {} 
    cursor.execute(f"SELECT user_password FROM user WHERE user_name = '{username}'")
    temp = cursor.fetchone()
    check_pw = bcrypt.check_password_hash(temp[0].encode('utf-8'),password)
    if not check_pw:
        return False
    else:
        cursor.execute(f"SELECT * FROM user WHERE user_name = '{username}'")
        temp = cursor.fetchone()
        user["user_id"] = temp[0]
        user["user_name"] = temp[1]
        user["total_value"] = temp[3]
    return user   

def generate_user(username, password):
    cursor.execute(f"SELECT user_name FROM user WHERE user_name = '{username}'")
    temp = cursor.fetchone()
    if temp != None:
        return False
    hash = bcrypt.generate_password_hash(password).decode('utf-8')
    cursor.execute(f'INSERT INTO user (user_name,user_password) VALUES ("{username}","{hash}")')
    cnx.commit()
    return True

def get_user(username):
    user = {}
    cursor.execute(f"SELECT * FROM user WHERE user_name = '{username}'")
    temp = cursor.fetchone()
    if temp == None:
        return None
    user["user_id"] = temp[0]
    user["user_name"] = temp[1]
    user["total_value"] = temp[3]
    return user

def delete_zero_stock(user_id):
    cursor.execute(f"DELETE FROM stock WHERE user_id = {user_id} AND shares = 0")
