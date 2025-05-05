import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv('DB_USER', 'bookstore_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'bookstore_pass')
DB_HOST = os.getenv('DB_HOST', 'db')
DB_NAME = os.getenv('DB_NAME', 'bookstore')
DB_PORT = os.getenv('DB_PORT', '3306')

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'secretkey')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuración de archivos estáticos
STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

# Asegurarse de que los directorios existan
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
