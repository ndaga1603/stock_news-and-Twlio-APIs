from decouple import config
from twilio.rest import Client
import os
import requests

STOCK = config("STOCK")
COMPANY_NAME = config("COMPANY_NAME")
API_KEY = config("API_KEY")
API_KEY2 = config("API_KEY2")


url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey={API_KEY}'
r = requests.get(url)
data = r.json()

new_data = data['Time Series (Daily)']
my_list = list(new_data.items())[1:3]
first = my_list[0][1]['4. close']
second = my_list[1][1]['4. close']
result = ((float(first) - float(second)) / float(second)) * 100

up_down = None
if result > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

if abs(result.__round__()) > 3:
    req = requests.get(f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&apiKey={API_KEY2}")
    tesla_data = req.json()
    new = list(tesla_data['articles'])
    working_data = new[:3]
  
    titles = []
    descriptions = []

    for x in working_data:
        tit = x['title']
        titles.append(tit)
        descr = x['description']
        descriptions.append(descr)
    
    account_sid = config("account_sid")
    auth_token = config("auth_token")

    for (title,description) in zip(titles,descriptions):

        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"{STOCK}: {up_down}{result.__round__()}%\n Headline: {title}\n Brief: {description}",
            from_=config("from"),
            to=config("to")
        )

        print(message.status)



