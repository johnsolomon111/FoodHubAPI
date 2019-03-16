from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy


server = Flask(__name__)
db = SQLAlchemy(server)

server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
server.secret_key = os.urandom(24)

from models import *
from app import *