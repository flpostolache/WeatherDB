from flask import Flask
from cities import cities
from countries import countries
from utils import *

srv = Flask(__name__)

srv.register_blueprint(cities)
srv.register_blueprint(countries, url_prefix='/api/')

if __name__ == '__main__':
	srv.run('0.0.0.0', debug=True, port='6000')