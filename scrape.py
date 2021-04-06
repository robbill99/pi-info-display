#!/usr/bin/python3

#!/usr/bin/python3
#Script to grab various data and display on piTFT
#Use getenv to get touchscreen taps in order to interate through screens
#do some pretty drawing stuff on piTFT
#find a way of making screen dim (resolder GPIO 18)
#also ways to minimise cpu load - it won't be doing much generally
#presumably will only turn on intermittently
#grab data only periodically to avoid sending loads of requests

import requests
from bs4 import BeautifulSoup

def get_data():

    covid_url="https://www.gov.je/Datasets/ListOpenData?ListName=COVID19&type=json"
    weather_url="https://www.gov.je/weather/Pages/Jersey-Forecast.aspx"

    r=requests.get(covid_url)
    covid=r.json()

    latest=covid["COVID19"][0]
    lastday=covid["COVID19"][1]

    covid_data = []
    covid_data.append(latest["Date"])
    covid_data.append(latest["KnownActiveCases"])

    total = latest["Totaltests"]

    #tests=int(latest["Totaltests"]) - int(lastday["Totaltests"])

    #obviously can make some lists of historic data and do calculations
    #perhaps python has some libraries which do data analysis
    #also a graphics library or graphing library

    #print(date, tests, active)

    r2=requests.get(weather_url)
    soup=BeautifulSoup(r2.text, "html.parser")

    content=soup.find("div", {"id": "forecastDetailWrapper"})

    weather = []
    for i in content.findAll("span"):
        weather.append(i.text)

    del weather[0]
    del weather[1]
    del weather[2]
    del weather[3]

    icon_details = content.find("img")
    icon_url = icon_details.attrs["src"]

    weather_icon_data = requests.get(icon_url)

    forecast = content.find("div", {"class": "forecastText"})
    forecast = forecast.text

    weather.append(forecast)

    return weather, covid_data, weather_icon_data


if __name__ == "__main__":
    print("Module only")
    pass
