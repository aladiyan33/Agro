import requests

API_KEY = "YOUR_OPENWEATHER_API_KEY"

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()
        desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"{city} weather: {desc}, {temp}°C"
    except:
        return "Weather data not available"
