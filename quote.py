import requests
import json


def update():
    url = 'https://quotes.rest/qod?category=life'
    api_token = "YOUR API KEY HERE"
    headers = {'content-type': 'application/json',
        'X-TheySaidSo-Api-Secret': format(api_token)}

    response = requests.get(url, headers=headers)
    #print(response)
    quotes=response.json()['contents']['quotes'][0]
    quotes = json.dumps(quotes, indent = 4)
    with open("quotes/quote.json", "w") as quotefile:
        quotefile.write(quotes)
        