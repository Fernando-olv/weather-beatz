""" Flask API """

import os

import requests
from dotenv import load_dotenv
from flask import Flask, request

app = Flask(__name__)


def temperature_genre(temperature):
    if temperature < 10:
        return "Classical"
    elif 10 <= temperature < 13:
        return "Pop"
    elif 13 <= temperature < 16:
        return "Samba"
    elif 16 <= temperature < 19:
        return "Punk"
    elif 19 <= temperature < 21:
        return "Sertanejo"
    elif 21 <= temperature < 24:
        return "Rock"
    elif 24 <= temperature < 27:
        return "Funk"
    elif 27 <= temperature < 30:
        return "Alternative"
    elif 30 <= temperature:
        return "Country"


def renew_access_token():
    """Renews Spotify Access Token using Client Secret"""
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {
        "grant_type": "client_credentials",
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }
    response = requests.post(url=url, headers=headers, data=body, timeout=10)
    response = response.json()
    SPOTIFY_ACCESS_TOKEN = response["access_token"]
    print(SPOTIFY_ACCESS_TOKEN)


def call_spotify_api(genre):
    """Calls Spotify and receives a playlist of the given genre"""
    url = "https://api.spotify.com/v1/browse/categories/{0}/playlists".format(genre)
    spotify_secret_key = os.getenv("SPOTIFY_ACCESS_TOKEN")
    headers = {"Authorization": "Bearer {0}".format(spotify_secret_key)}
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        return str(response.json()["playlists"]["items"][0]["external_urls"]["spotify"])

    print(f"Error Spotify: {response.status_code} - {response.reason}")


def get_weather(url):
    """Function to call Open Weather's API and save the response into a JSON"""
    openweather_secret_key = os.getenv("OPENWEATHER_SECRET_KEY")
    response = requests.get(url + "&APPID=" + openweather_secret_key, timeout=10)
    if response.status_code == 200:
        return response.json()["main"]["temp"]

    print(f"Error OpenWeather: {response.status_code} - {response.reason}")


@app.route("/city/<city_name>", methods=["GET"])
def city(city_name):
    """
    Return a playlist based on the city's temperature

    :param city_name: user given city name
    :return: json with playlist, status code and status message
    """
    city_url = (
        "https://api.openweathermap.org/" "data/2.5/weather?q={0}" ",BR&units=metric"
    )
    city_url = city_url.format(city_name)
    weather_data = get_weather(city_url)
    genre = temperature_genre(weather_data)
    print("temperature:" + str(weather_data))
    print("genre:" + genre)
    playlist = call_spotify_api(genre)
    if playlist is not None:
        return {
            "playlist": playlist,
            "status_code": 200,
            "status_message": "Succeed",
            "genre": genre,
        }

    return {"status_code": 500, "message": "Bad Request"}


@app.route("/coordinates", methods=["GET"])
def coordinates():
    """Return a playlist based on the coordinate's temperature"""
    coordinates_url = (
        "https://api.openweathermap.org"
        "/data/2.5/weather?lat={0}&lon={1}"
        "&exclude=minutely,hourly,daily,alerts"
        "&units=metric"
    )
    latitude = request.args.get("latitude")
    longitude = request.args.get("longitude")
    coordinates_url = coordinates_url.format(latitude, longitude)
    weather_data = get_weather(coordinates_url)
    genre = temperature_genre(weather_data)
    playlist = call_spotify_api(genre)
    if playlist is not None:

        return {"playlist": playlist, "status_code": 200, "status_message": "Succeed"}

    return {"status_code": 500, "message": "Bad Request"}


if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)
