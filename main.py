import requests
import datetime as dt
from twilio.rest import Client

STOCK = "TSLA" #Any stock symbol
COMPANY_NAME = "Tesla Inc" #Stock company name
AV_key = "CWIBBNOKLPHSII7K" 
News_key = "96a4c7252a114bb09c0dfa3c9df7a2eb"
account_sid = "<twilio account ssid>"
auth_token = "<twilio auth token>"
client = Client(account_sid, auth_token)

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    # "outputsize": "full",
    "apikey": AV_key
}
response = requests.get(url="https://www.alphavantage.co/query", params=params)
data = response.json()
today = str(dt.datetime.today())

print(data["Time Series (Daily)"])
dates = list(data["Time Series (Daily)"].keys())
yesterday = float(data["Time Series (Daily)"][dates[0]]["4. close"])
dby = float(data["Time Series (Daily)"][dates[1]]["4. close"])
price_change = yesterday - dby if yesterday > dby else dby - yesterday

params2 = {
    "q": "tesla",
    "from": "2022-8-17",
    "sortBy": "relevency",
    "apiKey": "96a4c7252a114bb09c0dfa3c9df7a2eb"
}

symbol = "🔺" if yesterday > dby else "🔻"
percent_change = round(price_change/float(data["Time Series (Daily)"][dates[1]]["4. close"]) * 100, 2)

if percent_change > 1.00:
    ## STEP 2: Use https://newsapi.org
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
    response2 = requests.get(url="https://newsapi.org/v2/everything", params=params2)
    news_data = response2.json()
    print(news_data)
    title = [news_data["articles"][i]["title"] for i in range(3)]
    description = [news_data["articles"][i]["description"] for i in range(3)]

    message = client.messages \
        .create(
        body=f"TSLA: {symbol}%{percent_change}\nTitle: {title[0]}\nArticle: {description[0]}\n\n"
             f"Title: {title[1]}\nArticle: {description[1]}\n\n"
             f"Title: {title[2]}\nArticle: {description[2]}",
        from_='<twilio phone number>',
        to='<reciever phone number>'
    )
    print(message.sid)
    print(percent_change)

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

