from functools import wraps
from flask import request, jsonify
import jwt
from config import Config

class JWTManager:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        self.secret_key = app.config['JWT_SECRET']
    
    def generate_token(self, user_id):
        return jwt.encode({'user_id': user_id}, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

jwt_manager = JWTManager()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'error': 'Token is missing or invalid'}), 401
        
        token = token.split(' ')[1]
        user_id = jwt_manager.verify_token(token)
        if not user_id:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        request.user_id = user_id
        return f(*args, **kwargs)
    return decorated