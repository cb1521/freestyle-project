import os
from dotenv import load_dotenv
from datetime import date

from app import APP_ENV
from app.weather_service import getting_daily_high, set_geography
from app.stock_service import last_close, set_stock_data
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

USER_NAME = os.getenv("USER_NAME", default="Player 1")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL_ADDRESS = os.getenv("SENDER_EMAIL_ADDRESS")


def send_email(subject="[Daily Briefing] This is a test", html="<p>Hello World</p>", recipient_address=SENDER_EMAIL_ADDRESS):
    """
    Sends an email with the specified subject and html contents to the specified recipient,

    If recipient is not specified, sends to the admin's sender address by default.
    """
    client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
    print("CLIENT:", type(client))
    print("SUBJECT:", subject)
    #print("HTML:", html)

    message = Mail(from_email=SENDER_EMAIL_ADDRESS, to_emails=recipient_address, subject=subject, html_content=html)
    try:
        response = client.send(message)
        print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
        print(response.status_code) #> 202 indicates SUCCESS
        return response
    except Exception as e:
        print("OOPS", type(e), e.message)
        return None


if __name__ == "__main__":


    # CAPTURE INPUTS

    user_country, user_zip = set_geography()
    print("COUNTRY:", user_country)
    print("ZIP CODE:", user_zip)

    user_symbol, user_shares= set_stock_data()
    print("SYMBOL:", user_symbol)
    print("SHARES:", user_shares)

    # FETCH DATA

    result = getting_daily_high(country_code=user_country, zip_code=user_zip) #capturing the weather
    if not result:
        print("INVALID GEOGRAPHY. PLEASE CHECK YOUR INPUTS AND TRY AGAIN!")
        exit()

    result1 = last_close(symbol=user_symbol) #capturing the stock
    if not result1:
        print("INVALID SYMBOL, PLEASE TRY AGAIN!")
        exit()

    # DISPLAY OUTPUTS


    #sending the email
    todays_date = date.today().strftime('%A, %B %d, %Y') 

    html = ""
    html += f"<h3>Good Morning, {USER_NAME}!</h3>"

    html += "<h4>Today's Date</h4>"
    html += f"<p>{todays_date}</p>"

    html += f"<p>The high in {result['city_name']} today will be {result['daily_high']}. </p>"
    html += f"<p>The most recent closing price for {user_symbol} today is {result1['latest_close']}. </p>"
    html += "<p>For more information on both the weather and the stocks, please visit https://freestyle-app.herokuapp.com/. </p>"
    html += "<p>Have a terrific day! </p>"
    html += "<ul>"

    send_email(subject="[Daily Email] Today's Crucial Information", html=html)
    
