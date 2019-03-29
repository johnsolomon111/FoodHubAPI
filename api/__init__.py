from flask import Flask, jsonify, request, make_response
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

server = Flask(__name__)

db = SQLAlchemy(server)

# server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
server.config['SECRET_KEY'] = 'thisisasecretkey'
# server.secret_key = os.urandom(24)	
server.debug = True

from api.models import *
from api.app import *