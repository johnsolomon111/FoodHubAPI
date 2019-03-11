from app import db, datetime
from werkzeug.security import generate_password_hash

class Customer(UserMixin, db.Model):
	__table__='customer'
	customer_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), nullable=False, unique=True)
	password = db.Column(db.String(80), nullable=False)
	firstname = db.Column(db.String(50), nullable=False)
	lastname = db.Column(db.String(50), nullable=False)
	contact_number = db.Column(db.String(11))
	gender = db.Column(db.String(6), nullable=False)
	images = db.relationship('Image', backref='image_customer')
	
	def __init__(self, username='', password='', firstname='', lastname='', contact_number='', gender=''):
		self.username = username
		self.password = generate_password_hash(password, method='sha256')
		self.firstname = firstname
		self.lastname = lastname
		self.contact_number = contact_number
		self.gender = gender

# FOREIGN KEY RESTAUANT TO OWNER (1 TO MANY)---------- (DONE) --------------
class Owner(UserMixin, db.Model):
	__table__='owner'
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
# FOREIGN KEY RESTAUANT TO OWNER (1 TO MANY)------- (DONE) ------------------
class Restaurant(db.model):
	__table__='restaurant'
	restaurant_id = db.Column(db.Integer, primary_key=True)
	restaurant_name = db.Column(db.String(30), nullable=False, unique=True)
	restaurant_type = db.Column(db.String(30), nullable=False)
	bio = db.Column(db.String(200), nullable=False)
	locations = db.Column(db.String(200), nullable=False)
	restaurant_owner_id = db.Column(db.Integer, db.ForeignKey(owner.owner_id))
	images = db.relationship('Image', backref='image_restaurant')

	def __init__(self, restaurant_name='', restaurant_type='', bio='', locations=''):
		self.restaurant_name = restaurant_name
		self.restaurant_type = restaurant_type
		self.bio = bio
		self.locations = locations

#NOT DONE FOREIGN KEY MISSING------------------------------------------------------------------------
class Menu(db.Model):
	__table__='menu'
	menu_id = db.Column(db.Integer, primary_key=True)
	price = db.Column(db.Double, nullable=False)
	item = db.Column(db.String, nullable=False)

	def __init__(self, price='', item=''):
		self.price = price
		self.item = item

#FOREIGN KEY RESTAURANT , CUSTOMER TO IMAGES (1 TO MANY) ------------------------------------------
class Image(db.Model):
	__table__='image'
	image_id = db.Column(db.Integer, primary_key=True)
	customer_image_filname = db.Column(db.String(50))
	restaurant_image_filename = db.Column(db.String(50))
	menu_image_filename = db.Column(db.String(50))
	image_restaurant_id = db.Column(db.Integer, db.ForeignKey(restaurant.restaurant_id))
	image_customer_id = db.Column(db.Integer, db.ForeignKey(customer.customer_id))

	def __init__(self, customer_image_filname = '', restaurant_image_filename='', menu_image_filename=''):
		self.customer_image_filname = customer_image_filname
		self.restaurant_image_filename = restaurant_image_filename
		self.menu_image_filename = menu_image_filename

class Booking(db.Model):
	__table__='booking'
	booking_id = db.Column(db.Integer, primary_key=True)
	booking_status = db.Column(db.String(20))
	booking_date = db.Column(db.DATE)
	pax_number = db.Column(db.Integer, nullable=False)

	def __init__(self, booking_status='', booking_date='', pax_number=''):
		self.booking_status = booking_status
		self.booking_date = booking_date
		self.pax_number = pax_number

class Category(db.Model):
	__table__='category'
	category_id = db.Column(db.Integer, primary_key=True)
	category_name = db.Column(db.String(20))

	def __init__(self, category_name=''):
		self.category_name = category_name

class Reviews(db.Model):
	__table__='reviews'
	comments = db.Column(db.String(100))
	star_rating = db.Column(db.Double)
	reviews_date = db.Column(db.DATE)

	def __init__(self, comments='', star_rating='',reviews_date=''):
		self.comments = comments
		self.star_rating = star_rating
		self.reviews_date = reviews_date
		
db.create_all()