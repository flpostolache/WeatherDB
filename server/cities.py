from flask import Blueprint, request, Response, json
from flask_expects_json import expects_json
from utils import *


cities = Blueprint('cities', __name__)
id = int(0)

schema = {
	"properties": {
		"idTara":{ "type": "integer"},
		"nume":	{ "type": "string" },
		"lat":	{ "type": "number" },
		"lon":	{ "type": "number" }
	},
	"required": ["nume", "lat", "lon", "idTara"]
}

schema_ex = {
	"properties": {
		"id":	{ "type": "integer"},
		"idTara": { "type": "integer" },
		"nume": { "type": "string" },
		"lat":	{ "type": "number" },
		"lon":	{ "type": "number" }
	},
	"required": ["nume", "lat", "lon", "id", "idTara"]
}

@cities.route('/', methods=["POST", "GET"])
@expects_json(schema, ignore_for=["GET"])
def post_get_cities():
	if request.method == "POST":
		global id
		id += 1
		values = '(' + f'{id}, ' + ', '.join([f'"{x}"' if type(x) == str else str(x) for x in list(request.get_json().values())]) + ')'
		columns = '('+ 'id, ' + ', '.join([x for x in request.get_json().keys()]) + ')'
		try:
			mycursor.execute(f'INSERT INTO Orase {columns} VALUES {values}')
			mydb.commit()
		except:
			id -= 1
			return Response(status=409)
		return Response(status=201, response=json.dumps({"id": id}))
	elif request.method == "GET":
		return_list = []
		keys_list = list(schema_ex["properties"].keys())
		mycursor.execute('select * from Orase')
		for x in mycursor.fetchall():
			return_list.append({keys_list[i]:x[i] for i in range(len(keys_list))})
		return Response(status=200, response=json.dumps(return_list))

@cities.route('/country/<id_tara>/', methods=["GET"])
def get_all_cities_by_country_id(id_tara):
	return_list = []
	keys_list = list(schema_ex["properties"].keys())
	mycursor.execute('SELECT * FROM Orase WHERE idTara = %s', [id_tara])
	for x in mycursor.fetchall():
		return_list.append({keys_list[i]:x[i] for i in range(len(keys_list))})
	return Response(status=200, response=json.dumps(return_list))

@cities.route('/<id>/', methods=["PUT", "DELETE"])
@expects_json(schema_ex, ignore_for=["DELETE"])
def put_delete(id):
	if request.method == "PUT":
		mycursor.execute('SELECT * FROM Orase WHERE id = %s', [id])
		entry = mycursor.fetchone()
		if not entry:
			return Response(status=404)
		body = request.get_json()
		try:
			mycursor.execute('UPDATE Orase SET id=%s, idTara=%s, nume=%s, lat=%s, lon=%s WHERE id=%s', [body['id'], body['idTara'], body['nume'], body['lat'], body['lon'], id])
			mydb.commit()
		except:
			return Response(status=409)
		return Response(status=200)
	elif request.method == "DELETE":
		try:
			_ = int(id)
		except:
			return Response(status=400)
		mycursor.execute('SELECT * FROM Orase WHERE id = %s', [id])
		entry = mycursor.fetchone()
		if not entry:
			return Response(status=404)
		mycursor.execute('DELETE FROM Orase WHERE id = %s', [id])
		mydb.commit()
		return Response(status=200)
