import requests
import random
import os 
from dotenv import load_dotenv

def get_random_city(amount,accu_apikey):

    city_index = random.randint(0, amount-1)

    url = f"http://dataservice.accuweather.com/locations/v1/topcities/{amount}?apikey={accu_apikey}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        city_object = data[city_index]
    
        
        return city_object['LocalizedName'], city_object['Country']['LocalizedName']

    else:
        print("Error has occured for the location get request")
        print(response.status_code)
        return None, None
    


# get the location key from accuweather
def get_location_key(city_name,accu_apikey):


 

    url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={accu_apikey}&q={city_name}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        return data[0]['Key']


    else:
        
        print("Error has occured for the location get request")
        print(city_name)
        return None
    

def get_daily_weather_stuff(loc_key,accu_apikey):
   

    url = f'http://dataservice.accuweather.com/forecasts/v1/daily/1day/{loc_key}?apikey={accu_apikey}'
    
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        Forecast_text = data['Headline']['Text']
        Daily_Forecast = data['DailyForecasts']

        Low_Temp = Daily_Forecast[0]['Temperature']['Minimum']["Value"]
        High_Temp = Daily_Forecast[0]['Temperature']['Maximum']['Value']

        return Forecast_text, Low_Temp, High_Temp

    else:
        print(f"Error has occured while gets{loc_key} weather")
        print(loc_key)
        return None, None, None




def weather_post():
    load_dotenv()
    accu_weather_apikey = os.getenv("accu_apikey")

    desired_city, Country = get_random_city(50, accu_weather_apikey)
    if desired_city is None or Country is None:
        return None,None,None,None,None

    location_key = get_location_key(desired_city, accu_weather_apikey)
    if location_key is None:
        return None,None,None,None,None

    Forecast_des, low_t, high_temp = get_daily_weather_stuff(location_key, accu_weather_apikey)
    if Forecast_des is None:
        return None,None,None,None,None

    return desired_city, Country, Forecast_des, low_t, high_temp


