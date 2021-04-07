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

    #I think this is quite slow on Pi 1 parsing the whole json dataset
    #Get the last 7 days - should be faster parsing info from a dict of 7 days rather than 200+
    covid_data = []
    for i in range(6):
        covid_data.append(covid["COVID19"][i])
    
    #Put last 7 days of required data categories into lists
    covid_date = []
    for i in range(6):
        covid_date.append(covid_data["Date"][i])
    
    covid_active = []
    for i in range(6):
        covid_date.append(covid_data["KnownActiveCases"][i])
    
    covid_totaltests = []
    for i in range(6):
        covid_totaltests.append(covid_data["Totaltests"][i])
    
    #calculate last number of tests
    
    if covid_totaltests[0] == 0:
        covid_newtests = 0
    else:
        count = 1
        while covid_totaltests[count] == 0:
            count += 1
        
        covid_newtests = covid_totaltests[count+1] - covid_totaltests[count]
        
        
    #latest=covid["COVID19"][0]
    #lastday=covid["COVID19"][1]  
    #covid_data.append(latest["Date"])
    #covid_data.append(latest["KnownActiveCases"])
    #total = latest["Totaltests"]
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

    #dump rubbish
    del weather[0]
    del weather[1]
    del weather[2]
    del weather[3]

    icon_details = content.find("img")
    icon_url = icon_details.attrs["src"]

    weather.append(icon_url)

    forecast = content.find("div", {"class": "forecastText"})
    forecast = forecast.text

    weather.append(forecast)

    return weather, covid_data


if __name__ == "__main__":
    print("Module only")
    pass
