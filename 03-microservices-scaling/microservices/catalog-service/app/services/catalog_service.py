from ..models import Book

class CatalogService:
    @staticmethod
    def get_all_books():
        return Book.query.all()
    
    @staticmethod
    def get_book(book_id):
        return Book.query.get(book_id)