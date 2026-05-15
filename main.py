import json

import requests

from fastapi import FastAPI, Request, HTTPException

from fastapi.responses import HTMLResponse

from fastapi.staticfiles import StaticFiles

from fastapi.templating import Jinja2Templates



app = FastAPI(title="WhatsTheWeather API")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})

@app.get("/api/weather")
def get_weather(city: str):
    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

    geocoding_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    geocoding_response = requests.get(geocoding_url, params=geocoding_params)

    if geocoding_response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail="Could not connect to the location service."
        )
    
    geocoding_data = geocoding_response.json()

    if "results" not in geocoding_data:
        raise HTTPException(
            status_code=404,
            detail="City not found."
        )
    
    location = geocoding_data["results"][0]
    latitude = location["latitude"]
    longitude = location["longitude"]
    city_name = location["name"]
    country = location.get("country", "Unknown")

    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "auto"
    }

    weather_response = requests.get(weather_url, params=weather_params)

    if weather_response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail="Could not connect to the weather service."
        )

    weather_data = weather_response.json()

    if "current" not in weather_data:
        raise HTTPException(
            status_code=404,
            detail="Weather data not found."
        )

    current_weather = weather_data["current"]

    units = weather_data["current_units"]

    return {
        "city": city_name,
        "country": country,
        "latitude": latitude,
        "longitude": longitude,
        "temperature": current_weather["temperature_2m"],
        "temperature_unit": units["temperature_2m"],
        "humidity": current_weather["relative_humidity_2m"],
        "wind_speed": current_weather["wind_speed_10m"],
        "wind_speed_unit": units["wind_speed_10m"],
        "time": current_weather["time"],
        "summary": f"The current temperature in {city_name} is {current_weather['temperature_2m']} {units['temperature_2m']} with a humidity of {current_weather['relative_humidity_2m']}% and wind speed of {current_weather['wind_speed_10m']} {units['wind_speed_10m']}."
    }