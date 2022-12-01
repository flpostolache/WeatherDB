from flask import Blueprint, request
from utils import *


cities = Blueprint('cities', __name__)

@cities.route('/api/cities/', methods=["GET"])
def get_cities():
	return "NICE", 200