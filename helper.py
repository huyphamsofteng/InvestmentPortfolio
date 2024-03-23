import yfinance as yf
import requests 
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

