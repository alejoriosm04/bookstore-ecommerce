from flask import Blueprint, request, jsonify
from .services.book_service import BookService
from .services.order_service import OrderService
from .models import db, Book, Order

order_routes = Blueprint('orders', __name__)

# Book CRUD Endpoints
@order_routes.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    required_fields = ['title', 'author', 'price', 'stock', 'seller_id']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    book = BookService.create_book(
        title=data['title'],
        author=data['author'],
        description=data.get('description', ''),
        price=data['price'],
        stock=data['stock'],
        seller_id=data['seller_id']
    )
    
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author
    }), 201

@order_routes.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    book = BookService.update_book(book_id, **data)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author
    }), 200

@order_routes.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    success = BookService.delete_book(book_id)
    if not success:
        return jsonify({'error': 'Book not found'}), 404
    
    return jsonify({'message': 'Book deleted'}), 200

# Order Endpoints
@order_routes.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    required_fields = ['user_id', 'book_id', 'quantity']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    order, error = OrderService.create_order(
        user_id=data['user_id'],
        book_id=data['book_id'],
        quantity=data['quantity']
    )
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'id': order.id,
        'total_price': order.total_price,
        'status': order.status
    }), 201

@order_routes.route('/orders/<int:order_id>/pay', methods=['POST'])
def pay_order(order_id):
    data = request.get_json()
    if not data or 'method' not in data:
        return jsonify({'error': 'Payment method required'}), 400
    
    payment, error = OrderService.process_payment(
        order_id=order_id,
        payment_method=data['method']
    )
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'id': payment.id,
        'amount': payment.amount,
        'status': payment.status
    }), 200