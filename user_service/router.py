from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from .models import db, User, Follow

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'], mobile_no=data['mobile_no'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'token': access_token, 'user_id': user.id}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@user_bp.route('/users/search', methods=['GET'])
def search_user():
    name = request.args.get('name')
    users = User.query.filter(User.username.ilike(f'%{name}%')).all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email, 'mobile_no': user.mobile_no} for user in users]), 200

@user_bp.route('/users/follow', methods=['POST'])
@jwt_required()
def follow_user():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    follow = Follow(follower_id=current_user_id, followed_id=data['followed_id'])
    db.session.add(follow)
    db.session.commit()
    return jsonify({'message': 'User followed successfully'}), 201

@user_bp.route('/users/unfollow', methods=['POST'])
@jwt_required()
def unfollow_user():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    follow = Follow.query.filter_by(follower_id=current_user_id, followed_id=data['followed_id']).first()
    if follow:
        db.session.delete(follow)
        db.session.commit()
        return jsonify({'message': 'User unfollowed successfully'}), 200
    return jsonify({'message': 'Follow relationship not found'}), 404
