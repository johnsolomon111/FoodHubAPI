from api import db
from werkzeug.security import generate_password_hash

class Customer(db.Model):
	__table__='customer'
	customer_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), nullable=False, unique=True)
	password = db.Column(db.String(80), nullable=False)
	firstname = db.Column(db.String(50), nullable=False)
	lastname = db.Column(db.String(50), nullable=False)
	contact_number = db.Column(db.String(11))
	gender = db.Column(db.String(6), nullable=False)

	def __init__(self, username='', password='', firstname='', lastname='', contact_number='', gender=''):
		self.username = username
		self.password = generate_password_hash(password, method='sha256')
		self.firstname = firstname
		self.lastname = lastname
		self.contact_number = contact_number
		self.gender = gender

# FOREIGN KEY RESTAUANT TO OWNER (1 TO MANY)---------- (DONE) --------------
class Owner(db.Model):
	__table__='owner'
	owner_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), nullable=False, unique=True)
	password = db.Column(db.String(80), nullable=False)
	firstname = db.Column(db.String(50), nullable=False)
	lastname = db.Column(db.String(50), nullable=False)
	contact_number = db.Column(db.String(11))
	gender = db.Column(db.String(6), nullable=False)
	
	def __init__(self, username='', password='', firstname='', lastname='', contact_number='', gender=''):
		self.username = username
		self.password = generate_password_hash(password, method='sha256')
		self.firstname = firstname
		self.lastname = lastname
		self.contact_number = contact_number
		self.gender = gender
		