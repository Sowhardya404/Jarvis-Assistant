# services/weather.py
import requests

def get_weather(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        weather = data['weather'][0]
        temp = main['temp']
        desc = weather['description']
        return f"The current temperature in {city} is {temp}°C with {desc}."
    else:
        return "Sorry, I couldn't get the weather information."
