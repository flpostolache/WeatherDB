import mysql.connector

mydb = mysql.connector.connect(host='localhost', password="password")


mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS Meteorologie")
mycursor.execute("USE Meteorologie")
mycursor.execute("CREATE TABLE IF NOT EXISTS Tari (id INT NOT NULL UNIQUE, nume VARCHAR(128) UNIQUE, lat DOUBLE(8, 3) NOT NULL, lon DOUBLE(8, 3) NOT NULL)")
mycursor.execute("CREATE TABLE IF NOT EXISTS Orase (id INT NOT NULL UNIQUE,idTara INT NOT NULL,nume VARCHAR(128),lat DOUBLE(8, 3) NOT NULL,lon DOUBLE(8, 3) NOT NULL,CONSTRAINT UC_City UNIQUE (idTara, nume),CONSTRAINT FK_Country FOREIGN KEY (idTara) REFERENCES Tari (id) ON DELETE CASCADE)")
mycursor.execute("CREATE TABLE IF NOT EXISTS Temperaturi (id INT(11) NOT NULL,valoare DOUBLE(8, 3) NOT NULL,timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,idOras INT NOT NULL,CONSTRAINT UC_Temp UNIQUE (timestamp, idOras),CONSTRAINT FK_City FOREIGN KEY (idOras) REFERENCES Orase (id) ON DELETE CASCADE)")