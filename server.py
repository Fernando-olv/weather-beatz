from flask import Flask
from flask import request
import requests

##Get's the secret from a local file.
API_path = "./.env"
with open(API_path,'r') as secret:
    appid = secret.read()

def call_api(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return "Erro: "+response.status_code


app = Flask(__name__)
@app.route('/city/<city_name>', methods=['GET'])
def city(city_name):
    city_url = "https://api.openweathermap.org/data/2.5/weather?q={0},BR&units=metric&APPID={1}"
    city_url = city_url.format(city_name,appid)
    weatherData = call_api(city_url)
    
    return str(weatherData["main"]["temp"])

@app.route('/coordinates', methods=['GET'])
def coordinates():
    coordinates_url = "https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&exclude=minutely,hourly,daily,alerts&units=metric&appid={2}"
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    coordinates_url = coordinates_url.format(latitude,longitude,appid)
    weatherData = call_api(coordinates_url)
    
    return str(weatherData["main"]["temp"])

if __name__ == '__main__':
    app.run(debug=True)
