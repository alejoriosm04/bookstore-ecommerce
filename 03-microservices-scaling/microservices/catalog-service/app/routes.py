from flask import Blueprint, jsonify
from .services.catalog_service import CatalogService
from .models import Book

catalog_routes = Blueprint('catalog', __name__)

@catalog_routes.route('/books', methods=['GET'])
def get_books():
    books = CatalogService.get_all_books()
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'description': book.description,
        'price': book.price,
        'stock': book.stock
    } for book in books]), 200

@catalog_routes.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = CatalogService.get_book(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'description': book.description,
        'price': book.price,
        'stock': book.stock
    }), 200