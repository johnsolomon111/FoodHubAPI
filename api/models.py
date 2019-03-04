from api import db

class Customer(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	lastname = db.Column(db.String(50))
	firstname = db.Column(db.String(50))
	email = db.Column(db.String(80), unique = True)
	password = db.Column(db.String(100))
	gender = db.Column(db.String(6))
	contact_num = db.Column(db.String(20), unique = True)


	def __init__(self, lastname, firstname, email, password, gender, contact_num):
		self.lastname = lastname
		self.firstname = firstname
		self.email = email
		self.password = password
		self.gender = gender
		self.contact_num = contact_num

class Owner(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	lastname = db.Column(db.String(50))
	firstname = db.Column(db.String(50))
	email = db.Column(db.String(80), unique = True)
	password = db.Column(db.String(100))
	gender = db.Column(db.String(6))
	contact_num = db.Column(db.String(20), unique = True)

	def __init__(self, lastname, firstname, email, password, gender, contact_num):
		self.lastname = lastname
		self.firstname = firstname
		self.email = email
		self.password = password
		self.gender = gender
		self.contact_num = contact_num

db.create_all()