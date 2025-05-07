from ..models import db, Book
from ..events.publishers.book_publisher import publish_book_event
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BookService:
    @staticmethod
    def create_book(title, author, description, price, stock, seller_id):
        book = Book(
            title=title,
            author=author,
            description=description,
            price=price,
            stock=stock,
            seller_id=seller_id
        )
        db.session.add(book)
        db.session.commit()
        
        publish_book_event('BOOK_CREATED', {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'description': book.description,
            'price': book.price,
            'stock': book.stock
        })
        
        return book
    
    @staticmethod
    def update_book(book_id, **kwargs):
        book = Book.query.get(book_id)
        if not book:
            return None
        
        for key, value in kwargs.items():
            if hasattr(book, key):
                setattr(book, key, value)
        
        db.session.commit()
        
        publish_book_event('BOOK_UPDATED', {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'description': book.description,
            'price': book.price,
            'stock': book.stock
        })
        
        return book
    
    @staticmethod
    def delete_book(book_id):
        book = Book.query.get(book_id)
        if not book:
            return False
        
        db.session.delete(book)
        db.session.commit()
        
        publish_book_event('BOOK_DELETED', {
            'id': book.id
        })
        
        return True
    
    @staticmethod
    def update_stock(book_id, quantity):
        book = Book.query.get(book_id)
        if not book:
            return None
        
        book.stock -= quantity
        db.session.commit()
        
        publish_book_event('STOCK_UPDATED', {
            'id': book.id,
            'stock': book.stock
        })
        
        return book