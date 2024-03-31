""" Flask API """

from flask import Flask
from flask import request
import requests

api_secret_path = "./.env"
with open(api_secret_path, encoding="utf-8") as secret:
    appid = secret.read()


def call_api(url):
    """Function to call APIs and save their response into a JSON"""
    response = requests.get(url, timeout=20)
    if response.status_code == 200:
        return response.json()
    else:
        return "Error: " + response.status_code


app = Flask(__name__)


@app.route("/city/<city_name>", methods=["GET"])
def city(city_name):
    """Return a playlist based on the city's temperature"""
    city_url = "https://api.openweathermap.org/data/2.5/weather?q={0},BR&units=metric&APPID={1}"
    city_url = city_url.format(city_name, appid)
    weather_data = call_api(city_url)
    return str(weather_data["main"]["temp"])


@app.route("/coordinates", methods=["GET"])
def coordinates():
    """Return a playlist based on the coordinate's temperature"""
    coordinates_url = "https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&exclude=minutely,hourly,daily,alerts&units=metric&appid={2}"
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    coordinates_url = coordinates_url.format(latitude, longitude, appid)
    weather_data = call_api(coordinates_url)
    return str(weather_data["main"]["temp"])


if __name__ == "__main__":
    app.run(debug=True)
