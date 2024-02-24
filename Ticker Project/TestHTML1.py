from flask import Flask, request, jsonify
import yfinance as yf
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/TickerGPT', methods=['POST'])
def TickerGPeT():
    data = request.json  # Get JSON data from the request
    ticker = data['ticker'].upper()  # Extract ticker and convert to uppercase
    print("Processing:", ticker)

    stats = yf.Ticker(ticker)

def TickerGPT():
    while True:
        user_tick = input("Please enter a ticker: ")
    ticker = user_tick.upper()
    print("Processing:", ticker)

    stats = yf.Ticker(ticker)  # Fetch data for the entered ticker symbol

    exchanges = ['xnas', 'xnys']  # List of exchanges to try
    data_found = False  # Flag to track if valid data has been found

    for exchange in exchanges:
        link = f"https://www.morningstar.com/stocks/{exchange}/{ticker}/quote"
        print("Trying:", link)
        parse_link = requests.get(link)
        soup = BeautifulSoup(parse_link.content, 'lxml')
        data = soup.find_all('p', class_='mdc-blockquote__content__mdc mdc-blockquote__content--small__mdc')

        if data:
            # If data is found, print it and break out of the loop
            current_price, bullPrice, bearPrice, finalPrice = stats.info.get('currentPrice'), stats.info.get('targetHighPrice'), stats.info.get('targetLowPrice'), stats.info.get('targetMeanPrice')

            recommendation = stats.info ['recommendationKey']
            print("Current Price:", current_price)
            for item in data:
                if data.index(item) == 0:
                    print("Bulls Say:", item.text)
                    print("Bull Price Target:", bullPrice)
                else:
                    print("Bears Say:", item.text)
                    print("Bear Price Target:", bearPrice)
                    print("")
                    print("Final Price Target:", finalPrice )
                    print("RECOMMENDATION:",recommendation )
            data_found = True
            break  # Exit the loop since valid data was found
    

    if not data_found:
        print('Enter a valid ticker')
    
    return jsonify(finalPrice="Fag")


if __name__ == '__main__':
    app.run(debug=True)

