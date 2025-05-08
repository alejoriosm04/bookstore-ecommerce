from flask import Blueprint, request, jsonify
from .services.auth_service import AuthService
from .models import db, User

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not all(k in data for k in ['name', 'email', 'password']):
        return jsonify({'error': 'Missing data'}), 400
    
    user, error = AuthService.register_user(
        data['name'],
        data['email'],
        data['password']
    )
    
    if error:
        return jsonify({'error': error}), 400
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User registered successfully',
        'user_id': user.id
    }), 201

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ['email', 'password']):
        return jsonify({'error': 'Missing email or password'}), 400
    
    user, error = AuthService.login_user(data['email'], data['password'])
    if error:
        return jsonify({'error': error}), 401
    
    token, error = AuthService.generate_token(user.id)
    if error:
        return jsonify({'error': 'Could not generate token'}), 500
    
    return jsonify({
        'token': token,
        'user_id': user.id,
        'name': user.name
    }), 200

@auth_routes.route('/users', methods=['GET'])
def list_users():
    try:
        users = User.query.all()
        return jsonify([{
            'id': user.id,
            'name': user.name,
            'email': user.email,
        } for user in users]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
