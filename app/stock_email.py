#importing necessary packages
import os
import requests
import json
import dotenv 
import datetime
from pandas import DataFrame
#import seaborn as sns
#import matplotlib.pyplot as plt

dotenv.load_dotenv() #establishing the .env file usage

TICKER_SYMBOL = os.getenv("TICKER_SYMBOL", default="MSFT")

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    
    Param: my_price (int or float) like 4000.444444
    
    Example: to_usd(4000.444444)
    
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71
#Info Inputs
#symbol_list= [] #empty list to store all of the stock tickers into for the loop
print("Welcome to the Robo Advisor! Feel free to enter up to 5 stock symbols at a time, one at a time, using the input below.")
#validating data
symbol= TICKER_SYMBOL
try:
    float(symbol) #making sure that the input is not a number
    print("Looks like you entered a number! Please try again.")
except ValueError:
    pass #letting everything that is not a number go through
if len(symbol)<1 or len(symbol)>5: #validating appropriate character length
    print("...You must enter a stock identifier that has between 1 to 5 characters. Try again!")
#print(type(symbol))

#for ticker in symbol_list: #looping through each ticker

def get_stock_data(symbol): 
    api_key= os.environ.get("ALPHAVANTAGE_API_KEY") #using the .env variable
    request_url= f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}" #getting the appropriate webpage
    #print(request_url)
    response= requests.get(request_url)
    if "https://www.alphavantage.co/documentation/" in str(response.text): #data validation method for invalid
        print("It seems as if you input an invalid stock symbol! This symbol will not generate any data. The rest of the symbols will still be generated.")
        quit()
    elif "https://www.alphavantage.co/premium/" in str(response.text): #data validation for exceeding the minute or daily limits
        print("You have either exceeded your calls per minute or your calls per day. Try again in a minute, or come back tomorrow!")
        quit()
    parsed_response=json.loads(response.text) #transforming the response into readable python data

    #setting up various variables and lists
    last_refreshed= parsed_response["Meta Data"]["3. Last Refreshed"]
    now= datetime.datetime.now()
    tsd= parsed_response["Time Series (Daily)"]
    dates=list(tsd.keys())
    latest_day= dates[0] #assumes latest day is first, may need to sort if not the case anymore
    latest_close= tsd[latest_day]["4. close"]
    highs=[]
    lows=[]
    for date in dates: #looping through and banking each variable into the lists
        high_price=tsd[date]["2. high"]
        low_price=tsd[date]["3. low"]
        highs.append(float(high_price))
        lows.append(float(low_price))
    recent_high= max(highs)
    recent_low= min(lows)
    chart_data=[] #setting up the line chart for later
    for date, daily_data in tsd.items():
        record = {
            "date": date,
            "close (in dollars)": float(daily_data["4. close"])
        }
        chart_data.append(record)

print("-------------------------")
print("SELECTED SYMBOL:", symbol.upper()) #symbol.upper() #stylistic purposes to be upper
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
#print("REQUEST AT:", now.strftime("%Y-%m-%d %I:%M %p")) #current date and time
print("-------------------------")
print("LATEST DATA FROM:", last_refreshed) #letting you know the most recent date
print("LATEST CLOSE:", to_usd(float(latest_close))) #displaying prices in usd
print("RECENT HIGH:", to_usd(float(recent_high)))
print("RECENT LOW:", to_usd(float(recent_low)))
print("-------------------------")
print("SHOWING A LINE CHART OF BEHAVIOR. TO CONTINUE, CLOSE THE IMAGE! DON'T FORGET TO SAVE!")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")