import pika
import json
from config import Config
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def publish_book_event(event_type, data):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=Config.RABBITMQ_HOST,
            credentials=pika.PlainCredentials(
                Config.RABBITMQ_USER,
                Config.RABBITMQ_PASS
            )
        ))
        channel = connection.channel()
        
        channel.exchange_declare(exchange='book_events', exchange_type='fanout')
        
        message = {
            'type': event_type,
            'data': data,
            'timestamp': str(datetime.utcnow())
        }
        
        channel.basic_publish(
            exchange='book_events',
            routing_key='',
            body=json.dumps(message)
        )
        
        logger.info(f"Published {event_type} event for book {data.get('id')}")
        connection.close()
    
    except Exception as e:
        logger.error(f"Error publishing event: {str(e)}")