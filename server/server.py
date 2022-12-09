from flask import Flask
from cities import cities
from countries import countries
from temperatures import temps
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('mysql',3306))
while result != 0:
	result = sock.connect_ex(('mysql',3306))
sock.close()

srv = Flask(__name__)

srv.register_blueprint(cities, url_prefix="/api/cities")
srv.register_blueprint(countries, url_prefix='/api/countries/')
srv.register_blueprint(temps, url_prefix='/api/temperatures/')

if __name__ == '__main__':
	srv.run('0.0.0.0', debug=True, port='6000')