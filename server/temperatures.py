from flask import Blueprint, request, Response, json
from flask_expects_json import expects_json
from utils import *


temps = Blueprint('temperatures', __name__)
id = int(0)

schema = {
	"properties": {
		"idOras": {"type": "integer"},
		"valoare": { "type": "number" }
	},
	"required": ["idOras", "valoare"]
}

response_format = ["id", "valoare", "timestamp"]

schema_ex = {
	"properties": {
		"id": { "type": "integer" },
		"idOras": { "type": "integer" },
		"valoare": { "type": "number" }
	},
	"required": ["id", "idOras", "valoare"]
}

@temps.route('/', methods=["POST", "GET"])
@expects_json(schema, ignore_for=["GET"])
def post_get_temps():
	if request.method == "POST":
		global id
		id += 1
		values = '(' + f'{id}, ' + ', '.join([f'"{x}"' if type(x) == str else str(x) for x in list(request.get_json().values())]) + ')'
		columns = '('+ 'id, ' + ', '.join([x for x in request.get_json().keys()]) + ')'
		try:
			mycursor.execute(f'INSERT INTO Temperaturi {columns} VALUES {values}')
			mydb.commit()
		except:
			id -= 1
			return Response(status=409)
		return Response(status=201, response=json.dumps({"id": id}))
	elif request.method == "GET":
		lat = request.args.get('lat', type=float)
		lon = request.args.get('lon', type=float)
		begin_date = request.args.get('from', type=str)
		until_date = request.args.get('until', type=str)
		
		query = 'SELECT id, valoare, DATE_FORMAT(timestamp, \'%Y-%m-%d\') FROM Temperaturi'
		timestamp_conds = []
		coordinates_conds = []

		if lat is not None:
			coordinates_conds.append(f'lat = {lat}')
		if lon is not None:
			coordinates_conds.append(f'lon = {lon}')
		if begin_date is not None:
			timestamp_conds.append(f'timestamp >= {begin_date}')
		if until_date is not None:
			timestamp_conds.append(f'timestamp <= {until_date}')

		if timestamp_conds or coordinates_conds:
			query += ' WHERE '
		if timestamp_conds:
			query += (' AND '.join(timestamp_conds))
		if timestamp_conds and coordinates_conds:
			query += ' AND '
		if coordinates_conds:
			query += ('idOras IN (SELECT id FROM Orase WHERE ' + ' AND '.join(coordinates_conds) + ')')
		return_list = []
		mycursor.execute(query)

		for x in mycursor.fetchall():
			return_list.append({response_format[i]:x[i] for i in range(len(response_format))})
		return Response(status=200, response=json.dumps(return_list))


@temps.route('/cities/<id_oras>/', methods=["GET"])
def get_cities(id_oras):
	return_list = []
	mycursor.execute(f'SELECT id, valoare, DATE_FORMAT(timestamp, \'%Y-%m-%d\') FROM Temperaturi where idOras={id_oras}')
	for x in mycursor.fetchall():
		return_list.append({response_format[i]:x[i] for i in range(len(response_format))})
	return Response(status=200, response=json.dumps(return_list))

@temps.route('/countries/<id_tara>/', methods=["GET"])
def get_countries(id_tara):
	return_list = []
	mycursor.execute(f'SELECT id, valoare, DATE_FORMAT(timestamp, \'%Y-%m-%d\') FROM Temperaturi where idOras in (SELECT id from Orase where idTara={id_tara})')
	for x in mycursor.fetchall():
		return_list.append({response_format[i]:x[i] for i in range(len(response_format))})
	return Response(status=200, response=json.dumps(return_list))

@temps.route('/<id>/', methods=["PUT", "DELETE"])
@expects_json(schema_ex, ignore_for=["DELETE"])
def put_delete(id):
	if request.method == "PUT":
		try:
			integer_id = int(id)
			integer_id_from_resp = request.get_json()['id']
			if integer_id != integer_id_from_resp:
				return Response(status=400)
		except:
			return Response(status=400)
		mycursor.execute('SELECT * FROM Temperaturi WHERE id = %s', [id])
		entry = mycursor.fetchone()
		if not entry:
			return Response(status=404)
		body = request.get_json()
		mycursor.execute('UPDATE Temperaturi SET id=%s, idOras=%s, valoare=%s WHERE id=%s', [body['id'], body['idOras'], body['valoare'], id])
		mydb.commit()
		return Response(status=200)
	elif request.method == "DELETE":
		try:
			_ = int(id)
		except:
			return Response(status=400)
		mycursor.execute('SELECT * FROM Temperaturi WHERE id = %s', [id])
		entry = mycursor.fetchone()
		if not entry:
			return Response(status=404)
		mycursor.execute('DELETE FROM Temperaturi WHERE id = %s', [id])
		mydb.commit()
		return Response(status=200)