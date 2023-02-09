import requests
from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY


def get_location_photo(city, state):
    headers = {"Authorization": PEXELS_API_KEY}

    url = f"https://api.pexels.com/v1/search?query={city}+{state}"
    resp = requests.get(url, headers=headers)
    return resp.json()["photos"][0]["url"]


def get_weather_data(city, state):
    geo_params = {"q": f"{city},{state},US", "appid": OPEN_WEATHER_API_KEY}
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    geo_resp = requests.get(geo_url, geo_params)
    json_geo_resp = geo_resp.json()

    try:
        latitude = json_geo_resp[0]["lat"]
        longitude = json_geo_resp[0]["lon"]
    except (KeyError, IndexError):
        return None

    weather_params = {
        "lat": latitude,
        "lon": longitude,
        "appid": OPEN_WEATHER_API_KEY,
        "units": "imperial",
    }

    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    weather_resp = requests.get(weather_url, weather_params)
    json_weather_resp = weather_resp.json()

    try:
        temperature = json_weather_resp["main"]["temp"]
        description = json_weather_resp["weather"][0]["description"]
        return {"temperature": temperature, "description": description}

    except (KeyError, IndexError):
        return None
