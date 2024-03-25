import yfinance as yf
import requests

import mysql.connector

def check_db():
    try:
        cnx = mysql.connector.connect(user='dpham', password='0918', host='127.0.0.1', database='stockbase')
        return True
    except Exception as e:
        return False

cnx = mysql.connector.connect(user='dpham', password='0918', host='127.0.0.1', database='stockbase')
cursor = cnx.cursor()

def create_db():
    cursor.execute("CREATE DATABASE IF NOT EXISTS stockbase")
    cursor.execute("CREATE TABLE IF NOT EXISTS stock (symbol CHAR(4), book_value FLOAT(7), shares INT(100), user_id INT(25), PRIMARY KEY (symbol))")
    cursor.execute("CREATE TABLE IF NOT EXISTS user (user_id INT(100) auto_increment, user_name CHAR(10),user_password CHAR(10), total_value FLOAT(7) DEFAULT 10000 ,PRIMARY KEY (user_id))")
    print(cnx)
    cnx.commit()
    
def check(symbol):
    try:
        response = requests.get(f'https://query2.finance.yahoo.com/v10/finance/quoteSummary/AAAA?modules=financialData%2CquoteType%2CdefaultKeyStatistics%2CassetProfile%2CsummaryDetail&corsDomain=finance.yahoo.com&formatted=false&symbol={symbol}&crumb=P8H2Ln3T.n2')
        # return response.status_code
        return 200
    except Exception as e: 
        return False

def get_price(symbol):
    call = yf.Ticker(f"{symbol}")
    if 'open' in call.info.keys():
        # return call.info['bid']
        return 300
    else:
        # return 0
        return 300  

def get_all_stocks(user_id):
    stocks=[]
    stock={}
    cursor.execute(f"SELECT * FROM stock WHERE user_id = {user_id}")
    temps = cursor.fetchall()
    for temp in temps:
        stock["symbol"] = temp[0].upper()
        stock["book_value"] = float(temp[1])
        stock["shares"] = int(temp[2])
        stock["user_id"] = int(temp[3])
        stock["market_value"] = stock["shares"] * get_price(stock["symbol"])
        stocks.append(stock.copy())
    return stocks.copy()
