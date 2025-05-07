import jwt
from datetime import datetime, timedelta
from flask import current_app
from ..models import User

class AuthService:
    @staticmethod
    def register_user(name, email, password):
        if User.query.filter_by(email=email).first():
            return None, 'Email already registered'
        
        new_user = User(name=name, email=email)
        new_user.set_password(password)
        
        return new_user, None
    
    @staticmethod
    def login_user(email, password):
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return None, 'Invalid credentials'
        
        return user, None
    
    @staticmethod
    def generate_token(user_id):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            token = jwt.encode(
                payload,
                current_app.config['JWT_SECRET'],
                algorithm='HS256'
            )
            return token, None
        except Exception as e:
            return None, str(e)