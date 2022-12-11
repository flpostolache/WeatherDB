from flask import Blueprint, request, Response, json
from flask_expects_json import expects_json
from utils import *


countries = Blueprint('countries', __name__)
id = int(0)

schema = {
	"properties": {
		"nume":	{ "type": "string" },
		"lat":	{ "type": "number" },
		"lon":	{ "type": "number" }
	},
	"required": ["nume", "lat", "lon"]
}

schema_ex = {
	"properties": {
		"id":	{ "type": "integer"},
		"nume": { "type": "string" },
		"lat":	{ "type": "number" },
		"lon":	{ "type": "number" }
	},
	"required": ["nume", "lat", "lon", "id"]
}

@countries.route('/', methods=["POST", "GET"])
@expects_json(schema, ignore_for=["GET"])
def post_get_countries():
	if request.method == "POST":
		global id
		id += 1
		values = '(' + f'{id}, ' + ', '.join([f'"{x}"' if type(x) == str else str(x) for x in list(request.get_json().values())]) + ')'
		columns = '('+ 'id, ' + ', '.join([x for x in request.get_json().keys()]) + ')'
		try:
			mycursor.execute(f'INSERT INTO Tari {columns} VALUES {values}')
			mydb.commit()
		except:
			id -= 1
			return Response(status=409)
		return Response(status=201, response=json.dumps({"id": id}))
	elif request.method == "GET":
		return_list = []
		keys_list = list(schema_ex["properties"].keys())
		mycursor.execute('select * from Tari')
		for x in mycursor.fetchall():
			return_list.append({keys_list[i]:x[i] for i in range(len(keys_list))})
		return Response(status=200, response=json.dumps(return_list))

@countries.route('/<id>/', methods=["PUT", "DELETE"])
@expects_json(schema_ex, ignore_for=["DELETE"])
def put_delete_countries(id):
	if request.method == "PUT":
		try:
			integer_id = int(id)
			integer_id_from_resp = request.get_json()['id']
			if integer_id != integer_id_from_resp:
				return Response(status=400)
		except:
			return Response(status=400)
		mycursor.execute('SELECT * FROM Tari WHERE id = %s', [id])
		entry = mycursor.fetchone()
		if not entry:
			return Response(status=404)
		body = request.get_json()
		try:
			mycursor.execute('UPDATE Tari SET id=%s, nume=%s, lat=%s, lon=%s WHERE id=%s', [body['id'], body['nume'], body['lat'], body['lon'], id])
			mydb.commit()
		except:
			return Response(status=409)
		return Response(status=200)
	elif request.method == "DELETE":
		mycursor.execute('SELECT * FROM Tari WHERE id = %s', [id])
		entry = mycursor.fetchone()
		if not entry:
			return Response(status=404)
		mycursor.execute('DELETE FROM Tari WHERE id = %s', [id])
		mydb.commit()
		return Response(status=200)
