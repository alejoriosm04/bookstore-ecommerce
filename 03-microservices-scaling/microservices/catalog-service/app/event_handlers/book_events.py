import pika
import json
from .. import db
from ..models import Book
from config import Config
import logging
from flask import current_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_book_event(ch, method, properties, body):
    with current_app.app_context():
        try:
            event = json.loads(body)
            event_type = event.get('type')
            book_data = event.get('data')
            
            if event_type == 'BOOK_CREATED':
                if not Book.query.get(book_data['id']):
                    book = Book(
                        id=book_data['id'],
                        title=book_data['title'],
                        author=book_data['author'],
                        description=book_data.get('description', ''),
                        price=book_data['price'],
                        stock=book_data['stock']
                    )
                    db.session.add(book)
            
            elif event_type == 'BOOK_UPDATED':
                book = Book.query.get(book_data['id'])
                if book:
                    book.title = book_data['title']
                    book.author = book_data['author']
                    book.description = book_data.get('description')
                    book.price = book_data['price']
                    book.stock = book_data['stock']
            
            elif event_type == 'BOOK_DELETED':
                book = Book.query.get(book_data['id'])
                if book:
                    db.session.delete(book)
            
            elif event_type == 'STOCK_UPDATED':
                book = Book.query.get(book_data['id'])
                if book:
                    book.stock = book_data['stock']
            
            db.session.commit()
            logger.info(f"Processed event: {event_type}")
        
        except Exception as e:
            logger.error(f"Error processing event: {str(e)}")
            db.session.rollback()

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=Config.RABBITMQ_HOST,
        credentials=pika.PlainCredentials(
            Config.RABBITMQ_USER,
            Config.RABBITMQ_PASS
        )
    ))
    channel = connection.channel()
    
    channel.exchange_declare(exchange='book_events', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='book_events', queue=queue_name)
    
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=handle_book_event,
        auto_ack=True
    )
    
    logger.info("Started RabbitMQ consumer for book events")
    channel.start_consuming()