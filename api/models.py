from api import db
from werkzeug.security import generate_password_hash

class Customer(db.Model):
	__tablename__ = 'customer'
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
class Owner(db.Model):
	__tablename__= 'owner'
	owner_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), nullable=False, unique=True)
	password = db.Column(db.String(80), nullable=False)
	firstname = db.Column(db.String(50), nullable=False)
	lastname = db.Column(db.String(50), nullable=False)
	contact_number = db.Column(db.String(11))
	gender = db.Column(db.String(6), nullable=False)
	restaurants = db.relationship('Restaurant', backref='restaurant_owner')
	
	def __init__(self, username='', password='', firstname='', lastname='', contact_number='', gender=''):
		self.username = username
		self.password = generate_password_hash(password, method='sha256')
		self.firstname = firstname
		self.lastname = lastname
		self.contact_number = contact_number
		self.gender = gender

class Restaurant(db.Model):
	__tablename__='restaurant'
	restaurant_id = db.Column(db.Integer, primary_key=True)
	restaurant_name = db.Column(db.String(30), nullable=False, unique=True)
	restaurant_type = db.Column(db.String(30), nullable=False)
	bio = db.Column(db.String(200), nullable=False)
	locations = db.Column(db.String(200), nullable=False)
	restaurant_owner_id = db.Column(db.Integer, db.ForeignKey('owner.owner_id'))

	def __init__(self, restaurant_name='', restaurant_type='', bio='', locations=''):
		self.restaurant_name = restaurant_name
		self.restaurant_type = restaurant_type
		self.bio = bio
		self.locations = locations

#db.create_all()