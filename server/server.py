from flask import Flask
from cities import cities
from countries import countries
from temperatures import temps

srv = Flask(__name__)

srv.register_blueprint(cities, url_prefix="/api/cities")
srv.register_blueprint(countries, url_prefix='/api/countries/')
srv.register_blueprint(temps, url_prefix='/api/temperatures/')

if __name__ == '__main__':
	srv.run('0.0.0.0', debug=True, port='6000')