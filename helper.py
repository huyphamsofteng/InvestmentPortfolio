import yfinance as yf
import requests

import mysql.connector

def create_db():
    cnx = mysql.connector.connect(user='dpham', password='0918', host='127.0.0.1', database='stockbase')
    cursor = cnx.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS stockbase")
    cursor.execute("CREATE TABLE IF NOT EXISTS stock (id INT(100) auto_increment, symbol CHAR(4), book_value FLOAT(7), market_value FLOAT(7), shares INT(100), user_id INT(25), PRIMARY KEY (id), FOREIGN KEY (user_id) REFERENCES user(user_id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS user (user_id INT(100) auto_increment,user_name CHAR(10),user_password CHAR(10),total_value FLOAT(7),PRIMARY KEY (user_id))")
    print(cnx)
    cnx.commit()
    cnx.close()
    
def check(symbol):
    try:
        response = requests.get(f'https://query2.finance.yahoo.com/v10/finance/quoteSummary/AAAA?modules=financialData%2CquoteType%2CdefaultKeyStatistics%2CassetProfile%2CsummaryDetail&corsDomain=finance.yahoo.com&formatted=false&symbol={symbol}&crumb=P8H2Ln3T.n2')
        if (response.status_code != 200):
            return False
        return True
    except Exception as e: 
        return False

def get_price(symbol):
    call = yf.Ticker(f"{symbol}")
    return call.info["ask"]

