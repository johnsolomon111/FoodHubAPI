from api import server, jsonify
from models import *

@server.route('/', methods=['GET'])
def index():
    return {"messege" : "Deployed"}


