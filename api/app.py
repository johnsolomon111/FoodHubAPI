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
    return 'Deployed!'

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
    restaurant = Restaurant(restaurant_name = data['restaurant_name'], 
                            restaurant_bio = data['restaurant_bio'],
                            restaurant_type = data['restaurant_type'],
                            location = data['location'])
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

@server.route('/restaurant/<restaurant_id>', methods=['DELETE'])
@token_required
def delete_restaurant(current_user,restaurant_id):
    restaurant = Restaurant.query.filter_by(restaurant_id=restaurant_id).first()
    if not restaurant:
        return jsonify({'message': 'No restaurant found.'})
    db.session.delete(restaurant)
    db.session.commit()
    return jsonify({'message':'Restaurant deleted!'})

 