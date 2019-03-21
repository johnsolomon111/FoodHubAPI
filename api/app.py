from api import server, jsonify, generate_password_hash, check_password_hash, request
from models import *

@server.route('/', methods=['GET'])
def index():
    return jsonify({"messege" : "Deployed"})

@server.route('/owner', methods=['POST'])
def register_owner():
	data = request.get_json()
	exist = Owner.query.filter_by(username = data['username']).first()
	if not exist: 
		new_user = Owner(username=data['username'],
					password=data['password'], 
					firstname=data['firstname'], 
					lastname=data['lastname'], 
					contact_number=data['contact_number'], 
					gender=data['gender'])
		db.session.add(new_user)
		db.session.commit()
		return jsonify({'messege' : 'New owner created'})
	else:
		return jsonify({'messege' : 'Owner already exist!'})

@server.route('/owner', methods=['GET'])
def get_owner():
	owners = Owner.query.all()
	
	results = []
	for owner in owners:
		owner_data = {}
		owner_data['owner_id'] = owner.owner_id
		owner_data['username'] = owner.username
		owner_data['password'] = owner.password
		owner_data['firstname'] = owner.firstname
		owner_data['lastname'] = owner.lastname
		owner_data['contact_number'] = owner.contact_number
		owner_data['gender'] = owner.gender
		results.append(owner_data)
	return jsonify({'Owners': results})

@server.route('/owner/<username>', methods=['GET'])
def get_one_owner(username):
	owner = Owner.query.filter_by(username=username).first()
	
	if not owner:
		return jsonify({'messege' : 'No owner found!'})
	owner_data = {}
	owner_data['owner_id'] = owner.owner_id
	owner_data['username'] = owner.username
	owner_data['password'] = owner.password
	owner_data['firstname'] = owner.firstname
	owner_data['lastname'] = owner.lastname
	owner_data['contact_number'] = owner.contact_number
	owner_data['gender'] = owner.gender	
	
	return jsonify({'owner' : owner_data})

@server.route('/customer', methods=['POST'])
def register_customer():
	data = request.get_json()
	exist = Customer.query.filter_by(username = data['username']).first()
	if not exist: 
		new_user = Customer(username=data['username'],
					password=data['password'], 
					firstname=data['firstname'], 
					lastname=data['lastname'], 
					contact_number=data['contact_number'], 
					gender=data['gender'])
		db.session.add(new_user)
		db.session.commit()
		return jsonify({'messege' : 'New customer created'})
	else:
		return jsonify({'messege' : 'Customer already exist!'})

@server.route('/customer/<username>', methods=['GET'])
def get_one_customer(username):
	customer = Customer.query.filter_by(username=username).first()
	
	if not customer:
		return jsonify({'messege' : 'No customer found!'})
	customer_data = {}
	customer_data['owner_id'] = customer.owner_id
	customer_data['username'] = customer.username
	customer_data['password'] = customer.password
	customer_data['firstname'] = customer.firstname
	customer_data['lastname'] = customer.lastname
	customer_data['contact_number'] = customer.contact_number
	customer_data['gender'] = customer.gender	
	
	return jsonify({'owner' : customer_data})
