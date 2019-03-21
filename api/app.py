from api import server
from models import *

@server.route('/', methods=['GET'])
def index():
    return '<h1>Deployed!</h1>'


