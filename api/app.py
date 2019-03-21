from flask import jsonify
from api import server
from models import *

@server.route('/', methods=['GET'])
def index():
    return jsonify("messege", "Deployed")


