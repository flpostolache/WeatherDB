# Tema 2 -  REST API & Docker

## Instalarea si rularea containerelor

In radacina proiectului sunt prezente doua foldere. Pentru copierea, construirea
si rularea imaginilor de docker, tot ce este necesar este sa va mutati in
folderul docker-compose si sa rulati comanda:

```console
foo@bar: docker-compose up --build
```

Parametrul build e optional atata timp cat nu exista deja o imagine de docker cu numele `my-server`.

## Containere

### API

Server-ul web este implementat in `Python` folosind `Flask`.

Fisierele sursa ale serverul se afla, impreuna cu fisierul `Dockerfile` in directorul `server/`. Imaginea pentru acest server poate fi creata si testata local, mergand in folderul server si ruland comanda `docker build -t <un_tag> .`. *API*-ul ruleaza pe portul `6000`. Pentru a-l rula local este necesar o baza de date ca mysql si setarea unor variablie de mediu.

Variabile necesare:

```vim
DB_HOSTNAME = localhost
MYSQL_PASSWORD = <parola_user-ului_de_pe_db>
MYSQL_USER = <numele_user-ului_local
MYSQL_DATABASE = Vreme
```

### Baza de date

Baza de date folosita pentru aceasta tema este o image de [mysql](https://hub.docker.com/_/mysql) pentru docker. Am ales-o deoarce am folosit-o si la BD semestrul trecut si pentru ca mi s-a parut suficienta si potrivita pentru cerintele din tema. Daca vrem sa ne conectam la baza de date putem sa o facem fie prin utilitar (explicat mai jos), fie prin orice alt utilitar care se va conecta prin portul 6969 al `localhost-ului` mapat la portul 3306 al containerullui cu baza de date.

Credentiale:

```vim
username: Mircea
password: password
```

### Utilitarul de gestiune

Utilitarul folosit este [adminer](https://hub.docker.com/_/adminer) Este destul de generic, usor de folosit si ofera o interfata destul de clara pentru a vedea datele. Pentru a ne conecta la utilitar este suficient sa deschidem orice browser si sa introducem ruta `localhost:42069` in bara de cautare. Acesta se conecteaza la portul 3306 al bazei de date. Configuratie necesara pentru a intra in baza de date:

```vim
System: MySQL
Server: mysql
Username: Mircea
Password: password
Database: Vreme
```

Valorile astea pot fi luate si din variabilele de mediu, dar am zis sa le trec si aici sa se gaseasca mai usor.

## Stergere

Scriptul `cleanup_script.sh` sterge din sistem toate resursele descarcate sau create (fisiere, volume, retele) de aplicatie. Va fi necesar sa introduci parola user-ului pentru a sterge folder-ul ce salveaza persistent baza de date.
