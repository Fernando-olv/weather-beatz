from flask import Flask
from flask import request

app = Flask(__name__)
@app.route('/city/<city_name>', methods=['GET'])
def city(city_name):
    return city_name
##To do, get the city_name variable from the Get path ex: city/Curitiba instead of using the request.args
##Now you can use the city's name refering to {city_name}

@app.route('/coordinates', methods=['GET'])
def coordinates():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    return "Latitude: "+latitude+" Longitude: "+longitude

if __name__ == '__main__':
    app.run(debug=True)
