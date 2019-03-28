from api import server, jsonify, request, generate_password_hash, check_password_hash, make_response
from models import *
import jwt
import datetime
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message':'Token is missing!'}), 401
        try: 
            data = jwt.decode(token, server.secret_key)
            current_user = Owner.query.filter_by(username = data['username']).first()
        except:
            return jsonify({'message':'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@server.route('/', methods=['GET'])
def index():
    return jsonify({"messege" : "Deployed"})

@server.route('/owner/register', methods=['POST'])
def register_owner():
	username = request.args['username']
	password = request.args['password']
	firstname = request.args['firstname']
	lastname = request.args['lastname']
	contact_number = request.args['contact_number']
	gender = request.args['gender']

	exist = Owner.query.filter_by(username = username).first()
	if not exist: 
		new_user = Owner(username=username,
					password=password, 
					firstname=firstname, 
					lastname=lastname, 
					contact_number=contact_number, 
					gender=gender)
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
	customer_data['customer_id'] = customer.customer_id
	customer_data['username'] = customer.username
	customer_data['password'] = customer.password
	customer_data['firstname'] = customer.firstname
	customer_data['lastname'] = customer.lastname
	customer_data['contact_number'] = customer.contact_number
	customer_data['gender'] = customer.gender	
	
	return jsonify({'customer' : customer_data})

	#================================================

@server.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify!', 401, {'WWW-Authenticate':'Basic realm = "Login required"'})
    user = Owner.query.filter_by(username=auth.username).first()
    if not user:
        return make_response('Could not verify!', 401, {'WWW-Authenticate':'Basic realm = "Login required"'})
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, server.secret_key)
        return jsonify({'token' : token.decode('UTF-8')})
    return make_response('Could not verify!', 401, {'WWW-Authenticate':'Basic realm = "Login required"'})


@server.route('/restaurants', methods=['GET'])
@token_required
def restaurants(current_user):
    restaurants = Restaurant.query.all()
    result = []
    for info in restaurants:
        info_data = {}
        info_data['restaurant_name'] = info.restaurant_name
        info_data['restaurant_bio'] = info.restaurant_bio
        info_data['restaurant_type'] = info.restaurant_type
        info_data['location'] = info.location
        result.append(info_data)
    return jsonify({'Restaurants' : result})

@server.route('/restaurant/<restaurant_id>', methods=['GET'])
def restaurant():
    return ''

@server.route('/restaurant', methods=['POST'])
@token_required
def add_restaurant(current_user):
    data = request.get_json()
    res_owner_id = Owner.query.filter_by(username= current_user)
    restaurant = Restaurant(restaurant_name = data['restaurant_name'], 
                            restaurant_bio = data['restaurant_bio'],
                            restaurant_type = data['restaurant_type'],
                            location = data['location'],
                            restaurant_owner_id = res_owner_id.owner_id)
    db.session.add(restaurant)
    db.session.commit()
    return jsonify({'message':'Restaurant added successfully!'})

@server.route('/restaurant/<restaurant_id>', methods=['PUT'])
@token_required
def update_restaurant(current_user,restaurant_id):
    data = request.get_json()
    updated_restaurant = Restaurant.query.filter_by(restaurant_id=restaurant_id).first()
    if not restaurant:
        return jsonify({'message': 'No restaurant found.'})
    updated_restaurant.restaurant_name = data['restaurant_name']
    updated_restaurant.restaurant_bio = data['restaurant_bio']
    updated_restaurant.restaurant_type = data['restaurant_type']
    updated_restaurant.location = data['location']
    db.session.commit()
    return jsonify({'message': 'Restaurant updated!'})

@server.route('/customer/<username>', methods=['PUT'])
@token_required
def update_customer(current_user, username):
	data = request.get_json()
	exist = Owner.query.filter_by(username = data['username']).first()
	this_user = Owner.query.filter_by(username = current_user.username)
	if not exist: 
		update_user = Customer(username=data['username'],
					password=data['password'], 
					firstname=data['firstname'], 
					lastname=data['lastname'], 
					contact_number=data['contact_number'], 
					gender=data['gender'])
		db.session.add(update_user)
		db.session.commit()
		return jsonify({'messege' : 'New customer created'})
	else:
		return jsonify({'messege' : 'Username already exist!'})


@server.route('/restaurant/<restaurant_id>', methods=['DELETE'])
@token_required
def delete_restaurant(current_user,restaurant_id):
    restaurant = Restaurant.query.filter_by(restaurant_id=restaurant_id).first()
    if not restaurant:
        return jsonify({'message': 'No restaurant found.'})
    db.session.delete(restaurant)
    db.session.commit()
    return jsonify({'message':'Restaurant deleted!'})
