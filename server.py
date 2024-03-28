from flask import Flask
from flask import request

app = Flask(__name__)
@app.route('/city/<city_name>', methods=['GET'])
def city(city_name):
    return city_name

@app.route('/coordinates', methods=['GET'])
def coordinates():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    return "Latitude: "+latitude+" Longitude: "+longitude

if __name__ == '__main__':
    app.run(debug=True)
