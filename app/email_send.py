import os
from dotenv import load_dotenv
from datetime import date

from app import APP_ENV
from app.weather_email import get_hourly_forecasts, set_geography
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

    # FETCH DATA

    result = get_hourly_forecasts(country_code=user_country, zip_code=user_zip)
    if not result:
        print("INVALID GEOGRAPHY. PLEASE CHECK YOUR INPUTS AND TRY AGAIN!")
        exit()

    # DISPLAY OUTPUTS

    todays_date = date.today().strftime('%A, %B %d, %Y')

    html = ""
    html += f"<h3>Good Morning, {USER_NAME}!</h3>"

    html += "<h4>Today's Date</h4>"
    html += f"<p>{todays_date}</p>"

    html += f"<h4>Weather Forecast for {result['city_name']}</h4>"
    html += "<ul>"
    for forecast in result["hourly_forecasts"]:
        html += f"<li>{forecast['timestamp']} | {forecast['temp']} | {forecast['conditions'].upper()}</li>"
    html += "</ul>"

    send_email(subject="[Daily Briefing] My Morning Report", html=html)
    
