from api import server
from models import *
from flask_restplus import Api, Resource

app = Api(server)

@server.route('/', methods=['GET'])
def index():
    return '<h1>Deployed!</h1>'


