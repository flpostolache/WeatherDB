import mysql.connector
from os import getenv
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
	try:
		result = sock.connect_ex((getenv("DB_HOSTNAME"),3306))
		if result == 0:
			sock.close()
			break
	except:
		pass


mydb = mysql.connector.connect(host=getenv("DB_HOSTNAME"), port=3306, passwd=getenv("MYSQL_PASSWORD"), user=getenv("MYSQL_USER"), db=getenv("MYSQL_DATABASE"))
mycursor = mydb.cursor()