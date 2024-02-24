from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import bullbearish


stock_info_access = bullbearish.BullishBearish()

app = Flask(__name__)
CORS(app)

@app.route('/TickerGPT', methods=['POST'])

def main():
    user_tick = request.json['text']

    finalInfo = ""
    bull_bear_list = stock_info_access.bullish_bearish_info(user_tick)
    for bull_bear_info in bull_bear_list:
        print(bull_bear_info)
        finalInfo += bull_bear_info + "\n"

    if len(bull_bear_list) > 0:
        stock_info_access.company_news()
        print(stock_info_access.chatGPT())
        finalInfo += stock_info_access.chatGPT()

    return jsonify(returnSentence = finalInfo)



if __name__ == '__main__':
    app.run(debug=True)

