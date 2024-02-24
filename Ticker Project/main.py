import bullbearish

stock_info_access = bullbearish.BullishBearish()

def main():
    while True:
        user_tick = input("Please input a stock ticker: ")
        bull_bear_list = stock_info_access.bullish_bearish_info(user_tick)
        for bull_bear_info in bull_bear_list:
            print(bull_bear_info)
        if len(bull_bear_list) > 0:
            stock_info_access.company_news()
            print(stock_info_access.chatGPT())




if __name__ == "__main__":
    main()