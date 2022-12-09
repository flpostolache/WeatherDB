import mysql.connector
from os import getenv

mydb = mysql.connector.connect(host='mysql', port=3306, passwd=getenv("MYSQL_PASSWORD"), user=getenv("MYSQL_USER"), db=getenv("MYSQL_DATABASE"))

mycursor = mydb.cursor()