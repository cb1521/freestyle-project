#importing necessary packages
import os
import requests
import json
import dotenv 
from dateutil.parser import parse as parse_datetime
from pandas import DataFrame
#import seaborn as sns
#import matplotlib.pyplot as plt

dotenv.load_dotenv() #establishing the .env file usage

TICKER_SYMBOL = os.getenv("TICKER_SYMBOL", default="MSFT")
STOCK_SHARES = os.getenv("STOCK_SHARES", default="1")

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    
    Param: my_price (int or float) like 4000.444444
    
    Example: to_usd(4000.444444)
    
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71

def format_date(dt_str):
    """
    Displays a datetime-looking string as the human friendly day.

    Params : dt_str (str) a datetime like "2021-03-29T21:00:00-04:00"

    See: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/modules/datetime.md
    """
    dt = parse_datetime(dt_str)
    return dt.strftime("%Y-%m-%d")

#Info Inputs
#symbol_list= [] #empty list to store all of the stock tickers into for the loop
#validating data
def set_stock_data():
    """
    Sets the stock data to use. Stock ticker and Number of shares.
    """
    symbol = TICKER_SYMBOL
    shares = STOCK_SHARES
    try:
        float(symbol) #making sure that the symbol is not a number
        print("Looks like you entered a number! Please try again.")
        quit()
    except ValueError:
        pass #letting everything that is not a number for the symbol go through, and letting everything that is a number for the shares go through
    if len(symbol)<1 or len(symbol)>5: #validating appropriate character length
        print("...You must enter a stock identifier that has between 1 to 5 characters. Try again!")
        quit()
    try:
        int(shares) #making sure the share number is an integer
        pass
    except ValueError:
        print("Please enter an integer for your stock shares!")
        quit()
    return symbol, shares

def last_close(symbol):

    """
    Returns the last closing price when you input the stock symbol
    """
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
    tsd= parsed_response["Time Series (Daily)"]
    dates=list(tsd.keys())
    latest_day= dates[0] #assumes latest day is first, may need to sort if not the case anymore
    latest_close= to_usd(float(tsd[latest_day]["4. close"]))
    return {"latest_close": latest_close}

def stock_growth(symbol, shares):

    """
    Shows how your investment has changed since yesterday, given a particular stock and a certain number of shares.
    """
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
    tsd= parsed_response["Time Series (Daily)"]
    dates=list(tsd.keys())
    latest_day= dates[0]
    previous_day= dates[1]
    latest_close= float(tsd[latest_day]["4. close"]) #getting various metrics to implement in conjunction with each other
    previous_close= float(tsd[previous_day]["4. close"])
    current_investor_value= latest_close*int(shares)
    previous_investor_value= previous_close*int(shares)
    stock_data=[]
    stock_data.append({
        "latest_close": to_usd(latest_close),
        "current_investor_value": to_usd(current_investor_value),
        "previous_investor_value": to_usd(previous_investor_value),
        "change_in_value": to_usd(current_investor_value - previous_investor_value)
    })
    return{"stock_data": stock_data}

def stock_time(symbol, shares):
    """
    Shows the past 20 closing prices with their days
    """
    api_key= os.environ.get("ALPHAVANTAGE_API_KEY") #using the .env variable
    request_url= f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}" #getting the appropriate webpage
    #print(request_url)
    response= requests.get(request_url)
    if "https://www.alphavantage.co/documentation/" in str(response.text): #data validation method for invalid
        print("It seems as if you input an invalid stock symbol! This symbol will not generate any data.")
        quit()
    elif "https://www.alphavantage.co/premium/" in str(response.text): #data validation for exceeding the minute or daily limits
        print("You have either exceeded your calls per minute or your calls per day. Try again in a minute, or come back tomorrow!")
        quit()
    parsed_response=json.loads(response.text) #transforming the response into readable python data
    tsd= parsed_response["Time Series (Daily)"]
    dates=list(tsd.keys())
    investment_trends= []
    for date in dates [0:20]: #looping through and banking each variable into the lists
        daily_close=tsd[date]["4. close"] #creating a list of dictionaries to analyze recent behavior
        investment_trends.append({
            "date": format_date(date),
            "daily_investment_close": to_usd(float(daily_close)*int(shares))
    })
    investment_trends.reverse()
    return{"investment_trends": investment_trends}

if __name__ == "__main__":
    user_symbol, user_shares= set_stock_data()
    
    # FETCH DATA

    result= last_close(symbol= user_symbol) #validations
    if not result:
        print("INVALID SYMBOL OR SHARES, PLEASE TRY AGAIN!")
        exit()

    result1 = stock_growth(symbol= user_symbol, shares= user_shares)
    if not result1:
        print("INVALID SYMBOL OR SHARES, PLEASE TRY AGAIN!")
        exit()
    
    result2 = stock_time(symbol= user_symbol, shares= user_shares)
    if not result2:
        print("INVALID SYMBOL OR SHARES, PLEASE TRY AGAIN!")
        exit()

    # DISPLAY OUTPUTS

    #putting it all together
    print("-----------------")
    print(f"THE LAST CLOSING PRICE FOR {user_symbol} STOCK IS {result['latest_close']}")
    print("-----------------")

    print("-----------------")
    for y in result1["stock_data"]:
        print(f"YOUR INVESTMENT IN {user_symbol} STOCK HAS CHANGED BY {y['change_in_value']}")
    print("-----------------")
    
    print("-----------------")
    print(f"THE PAST MONTH OF DATA FOR {user_symbol}...")
    print("-----------------")

    for x in result2["investment_trends"]:
        print(x["date"], "|", x["daily_investment_close"])
