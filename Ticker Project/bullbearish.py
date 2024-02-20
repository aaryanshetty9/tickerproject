from bs4 import BeautifulSoup
import requests
from config import NEWS_API_KEY
from config import OPEN_AI_API_KEY
import yfinance as yf
from openai import OpenAI

#Purpose of this class is to get Bullish Bearish data from morning face and relevent news from NewsAPI to display to the user based on a ticker they input. 
class BullishBearish:
    news_api_key = NEWS_API_KEY
    client = OpenAI(api_key = OPEN_AI_API_KEY)
    gpt_model="gpt-3.5-turbo"


    def __init__(self):
        #user tick is the ticker the user will input
        self.user_tick = None
        #company info is up to date news about the company and their stock health
        self.company_info = None

    def bullish_bearish_info(self, tick = None):
        #recieve ticker and assign it to instance variable
        self.user_tick = tick
        #make ticker uppercase to make link valid in the future
        ticker = self.user_tick.upper()
        print("Processing:", ticker)
        #different exchanges morning star uses to organize stocks, xnas = nasdaq, xnys = nyse
        exchanges = ['xnas', 'xnys'] 
        #if stock doesn't exist, this will be used later
        data_found = False  
        #loop through both exhanges and check if there is a valid link
        for exchange in exchanges:
            #baselink for morningstar
            link = f"https://www.morningstar.com/stocks/{exchange}/{ticker}/quote"
            #line 35-38 scrapes data from HTML
            parse_link = requests.get(link)
            soup = BeautifulSoup(parse_link.content, 'lxml')
            data = soup.find_all('p', class_='mdc-blockquote__content__mdc mdc-blockquote__content--small__mdc')
            #create list to append data
            data_list = []
            #41-48 appends bullish bearish data to data_list
            if data:
                    for item in data:
                        if data.index(item) == 0:
                            data_list.append("Bulls Say: " + item.text + " (Morningstar)")
                        else:
                            data_list.append("Bears Say: " + item.text + " (Morningstar)")
                    data_found = True
                    break  
        #if invalid stock is inputted
        if not data_found:
            print('Enter a valid ticker')
        #return bullish bearish data from morning star
        return data_list
    
    #this method retrieves stock data from yahoo finance api
    def get_yahoo_data(self, tick = None):
        #if ticker doesnt exist, ticker can be inputted through the parameter if this method
        if self.user_tick == None:
            self.user_tick = tick
        self.company_info = yf.Ticker(self.user_tick)
        return self.company_info
    


    def company_news(self, tick = None):
        if self.user_tick == None:
            self.user_tick = tick
        #company name retrieval
        company_name = self.get_yahoo_data().info['shortName']
        #news_query = company_name + " AND (new product OR stock)"
        #query for NewsAPi
        news_query = company_name
        #news_query = company_name + ' AND (innovations OR technology OR stock).'
        base_url = "https://newsapi.org/v2/everything"
        #retrive 20 of the latest articles from NewsAPI
        parameter = {
        'q': news_query, 
        'pageSize': 20,  
        'apiKey': BullishBearish.news_api_key,
        'language': 'en',  
        'sortBy': 'publishedAt'
          }
        #get article info
        article_info = requests.get(base_url, params=parameter)
        #debugging if articles are not fetched
        if article_info.status_code == 200:
            articles = article_info.json().get('articles', [])
        else:
            print("Failed to fetch articles. Status code:", article_info.status_code) 
        
        #list comprehension that adds article description, date published, and link from article
        articles = [str(article['description']) + str(article['publishedAt']) + str(article['url']) for article in articles]
        
        #query for chatGPT API
        return "Article list " + str(articles) + "  Summarize the articles above in 2 bullet points, the first bullet point should be about recent products + innovations or news, the next bullet point should be information on how the stock is doing today. The information should ONLY be about " + company_name + " and each bullet point should have different info. Include the publication date and url of the article alongside the bullet point summarizing the information extracted from it. Use the format info - date m/d/yr - url."
    
    
    def chatGPT(self):
        #query for chatGPT API
        enclosed_prompt = self.company_news()
        response = BullishBearish.client.chat.completions.create(
        model= BullishBearish.gpt_model,
        max_tokens = 1000,
        messages=[
            {"role": "user", "content": enclosed_prompt},
                ])
        response_message = response.choices[0].message.content
        #company news and company stock news returned
        return str(response_message)
        
        


        

    
           