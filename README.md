# freestyle-project

This README file was adapted from Professor Michael Rossetti's README for his daily briefing repo. Link is [here](https://github.com/prof-rossetti/daily-briefings-py).

Operates as a customized email service containing the day's high temperature, as well as the latest stock price for a stock of interest. Is also deployable as a web app, which has many more features, including an hourly breakdown of the weather, a 7-day forecast, a summary of your holdings in a specific stock, and a look at the past 20 closes of that same stock. This is the simple app, and here's what you need to do to use it.

## Installation

Fork [this repo](https://github.com/cb1521/freestyle-project), then clone or download the forked repo onto your local computer (for example to the Desktop), then navigate there from the command-line:

```sh
cd ~/Desktop/freestyle-project/
```

Use Anaconda to create and activate a new virtual environment, perhaps called "freestyle-env":

```sh
conda create -n freestyle-env python=3.8
conda activate freestyle-env
```

Then, within an active virtual environment, install package dependencies:

```sh
pip install -r requirements.txt
```

## Configuration

Follow these [SendGrid setup instructions](https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/packages/sendgrid.md#setup) to sign up for a SendGrid account, configure your account's email address (i.e. `SENDER_EMAIL_ADDRESS`), and obtain an API key (i.e. `SENDGRID_API_KEY`). You will also want to sign up for an Alphavantage API for the stocks, you can do that [here]()

Create a new file called ".env" in the root directory of this repo, and paste the following contents inside, using your own values as appropriate:

```sh
# these are example contents for the ".env" file:

# required vars:
ALPHAVANTAGE_API_KEY= "_______________"
SENDGRID_API_KEY= "_______________"
SENDER_EMAIL_ADDRESS= "_______________"
USER_NAME= "_______________"
COUNTRY_CODE= "_______________"
ZIP_CODE= "_______________"
TICKER_SYMBOL= "_______________"
STOCK_SHARES= "_______________"

```

## Usage

If you want to use the terminal, use these commands to do so:

To get weather outputs:

```sh
python -m app.weather_service

```

To get stock outputs:

```sh
python -m app.stock_service
```

> NOTE: the SendGrid emails might first start showing up in spam, until you designate them as coming from a trusted source (i.e. "Looks Safe")

Sending some of the weather and stock info in the email:

```sh
python -m app.email_send
```

## Web App

```sh
# mac:
FLASK_APP=web_app flask run

# windows:
export FLASK_APP=web_app
flask run

```

## Testing

Running tests:

```sh
pytest

# in CI mode:
CI=true pytest
```

## Deploying

You can send the web app to a remote server, as well as automate the daily email.

# Deploying to Heroku

## Prerequisites

If you haven't yet done so, [sign up for a Heroku account](https://github.com/prof-rossetti/intro-to-python/blob/master/notes/clis/heroku.md#prerequisites) and [install the Heroku CLI](https://github.com/prof-rossetti/intro-to-python/blob/master/notes/clis/heroku.md#installation), and make sure you can login and list your applications.

```sh
heroku login # just a one-time thing when you use heroku for the first time

heroku apps # at this time, results might be empty-ish
```

## Server Setup

> IMPORTANT: run the following commands from the root directory of your repository!

Use the online [Heroku Dashboard](https://dashboard.heroku.com/) or the command-line (instructions below) to [create a new application server](https://dashboard.heroku.com/new-app), specifying a unique name (e.g. "freestyle-app", but yours will need to be different):

```sh
heroku create freestyle-app # choose your own unique name!
```

Verify the app has been created:

```sh
heroku apps
```

Also verify this step has associated the local repo with a remote address called "heroku":

```sh
git remote -v
```

## Server Configuration

Before we copy the source code to the remote server, we need to configure the server's environment in a similar way we configured our local environment.

Instead of using a ".env" file, we will directly configure the server's environment variables by either clicking "Reveal Config Vars" from the "Settings" tab in your application's Heroku dashboard, or from the command line (instructions below):

![a screenshot of setting env vars via the app's online dashboard](https://user-images.githubusercontent.com/1328807/54229588-f249e880-44da-11e9-920a-b11d4c210a99.png)

```sh
# or, alternatively...

# get environment variables:
heroku config # at this time, results might be empty-ish

# set environment variables:

heroku config:set SENDGRID_API_KEY="_________"
heroku config:set SENDER_EMAIL_ADDRESS="_________"
heroku config:set TICKER_SYMBOL="_________"
heroku config:set ALPHAVANTAGE_API_KEY="_________"
heroku config:set STOCK_SHARES="_________"
heroku config:set COUNTRY_CODE="_________"
heroku config:set ZIP_CODE="_________"
heroku config:set USER_NAME="_________"
```

At this point, you should be able to verify the production environment has been configured with the proper environment variable values:

```sh
heroku config
```

## Deploying

After this configuration process is complete, you are finally ready to "deploy" the application's source code to the Heroku server:

```sh
git push heroku main
```

> NOTE: any time you update your source code, you can repeat this deployment command to upload your new code onto the server

## Running the Script in Production

Once you've deployed the source code to the Heroku server, login to the server to see the files there, and take an opportunity to test your ability to run the script that now lives on the server:

```sh
heroku run bash # login to the server
# ... whoami # see that you are not on your local computer anymore
# ... ls -al # optionally see the files, nice!
# ... python -m app.daily_briefing # see the output, nice!
# ... exit # logout

# or alternatively, run it from your computer, in "detached" mode:
heroku run "python -m app.daily_briefing"
```

## Scheduling the Script

Finally, provision and configure the server's "Heroku Scheduler" resource to run the notification script at specified intervals, for example once per day in the morning.

From the "Resources" tab in your application's Heroku dashboard, search for an add-on called "Heroku Scheduler" and provision the server with a free plan.

![a screenshot of searching for the resource](https://user-images.githubusercontent.com/1328807/54228813-59ff3400-44d9-11e9-803e-21fbd8f6c52f.png)

![a screenshot of provisioning the resource](https://user-images.githubusercontent.com/1328807/54228820-5e2b5180-44d9-11e9-9901-13c538a73ac4.png)

> NOTE: if doing this for the first time, Heroku may ask you to provide billing info. Feel free to provide it, as the services we are using to complete this exercise are all free, and your card should not be charged!

Finally, click on the provisioned "Heroku Scheduler" resource from the "Resources" tab, then click to "Add a new Job". When adding the job, choose to execute the designated python command (`python -m app.daily_briefing`) at a scheduled interval (e.g. every 10 minutes), and finally click to "Save" the job:

![a screenshot of the job configuration menu](https://user-images.githubusercontent.com/1328807/54229044-da259980-44d9-11e9-91d8-51773499cbfb.png)


## It's Alive!

Congratulations, you have just deployed a software service!

Monitor your inbox over the specified time period and witness your notification service in action!