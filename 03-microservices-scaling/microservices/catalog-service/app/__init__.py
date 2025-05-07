from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import pika
import threading

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .routes import catalog_routes
    app.register_blueprint(catalog_routes)
    
    # Start RabbitMQ consumer in background
    if not app.config.get('TESTING'):
        from .event_handlers.book_events import start_consumer
        thread = threading.Thread(target=start_consumer, daemon=True)
        thread.start()
    
    return app