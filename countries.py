from flask import Blueprint, request, Response, json
from flask_expects_json import expects_json
from utils import *


countries = Blueprint('countries', __name__)

schema = {
  "properties": {
    "nume": { "type": "string" },
    "lat": { "type": "number" },
    "lon": { "type": "number"}
  },
  "required": ["nume", "lat", "lon"]
}

@countries.route('/countries/', methods=["POST", "GET"])
@expects_json(schema, ignore_for=["GET"])
def post_get_countries():
	if request.method == "POST":
		values = '(' + ', '.join([f'"{x}"' if type(x) == str else str(x) for x in list(request.get_json().values())]) + ')'
		columns = '(' + ', '.join([x for x in request.get_json().keys()]) + ')'
		try:
			mycursor.execute(f'INSERT INTO Tari {columns} VALUES {values}')
			mydb.commit()
		except:
			return Response(status=409)
		mycursor.execute('SELECT LAST_INSERT_ID()')
		return Response(status=201, response=json.dumps({"id": mycursor.fetchone()[0]}))
	elif request.method == "GET":
		return_list = []
		keys_list =["id"]
		keys_list.extend(list(schema["properties"].keys()))
		mycursor.execute('select * from Tari;')
		for x in mycursor.fetchall():
			return_list.append({keys_list[i]:x[i] for i in range(len(keys_list))})
		return Response(status=200, response=str(return_list))

@countries.route('/countries/<id>/', methods=["PUT", "DELETE"])
def put_delete_countries(id):
	try:
		int_id = int(id)
	except:
		return Response(status=404)
	
	mycursor.execute('SELECT * FROM Tari WHERE id = %s', [id])
	entry = mycursor.fetchone()
	if not entry:
		return Response(status=404)
	body = request.get_json()
	print(body)
	mycursor.execute('UPDATE Tari SET nume=%s, lat=%s, lon=%s WHERE id=%s', [body['nume'], body['lat'], body['lon'], id])
	mydb.commit()
	#print(request.get_json())

	return Response(status=200)
