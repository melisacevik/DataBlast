import requests
import csv


# QUESTION 1 #

url = "https://api.currencyfreaks.com/v2.0/rates/latest?apikey=cf606545094e42c0a52fc26798acfb55"

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

ourdata = []
def get_exchange_rates():

    try:
        response = requests.request("GET", url, headers=headers, data={})
        data = response.json()

        if response.status_code == 200:
            date = data.get('date', {})
            rates = data.get('rates', {})

            for currency, rate in rates.items():
                listing = [date, currency, rate]
                ourdata.append(listing)
        else:
            print(f"Error code: {response.status_code}, Error message: {data.get('error', 'Invalid error')}")
    except Exception as e:
        print(f"Error occurred: {e}")

get_exchange_rates()
print(ourdata)
with open('currencies.csv','w',encoding='UTF-8',newline='') as f:
    writer = csv.writer(f)

    writer.writerow(['date','name','rate'])
    writer.writerows(ourdata)

print('done')

