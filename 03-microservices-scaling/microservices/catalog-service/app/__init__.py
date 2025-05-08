from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import threading
import logging

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .routes import catalog_routes
    app.register_blueprint(catalog_routes)
    
    with app.app_context():
        db.create_all()
    
    if not app.config.get('TESTING'):
        start_rabbitmq_consumer(app)
    
    return app

def start_rabbitmq_consumer(app):
    from .event_handlers.book_events import start_consumer
    
    def consumer_wrapper():
        with app.app_context():
            logging.info("Starting RabbitMQ consumer with app context")
            start_consumer()
    
    thread = threading.Thread(
        target=consumer_wrapper,
        daemon=True
    )
    thread.start()
    logging.info(f"Started RabbitMQ consumer thread {thread.name}")