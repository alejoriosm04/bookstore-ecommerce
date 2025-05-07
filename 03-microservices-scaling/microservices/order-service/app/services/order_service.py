from ..models import db, Order, Book, Payment
from ..services.book_service import BookService
from ..events.publishers.book_publisher import publish_book_event

class OrderService:
    @staticmethod
    def create_order(user_id, book_id, quantity):
        book = Book.query.get(book_id)
        if not book:
            return None, 'Book not found'
        
        if book.stock < quantity:
            return None, 'Insufficient stock'
        
        total_price = book.price * quantity
        
        order = Order(
            user_id=user_id,
            book_id=book_id,
            quantity=quantity,
            total_price=total_price
        )
        db.session.add(order)
        
        # Update book stock
        BookService.update_stock(book_id, quantity)
        
        db.session.commit()
        return order, None
    
    @staticmethod
    def process_payment(order_id, payment_method):
        order = Order.query.get(order_id)
        if not order:
            return None, 'Order not found'
        
        if order.status != 'pending':
            return None, 'Order already processed'
        
        payment = Payment(
            order_id=order_id,
            amount=order.total_price,
            method=payment_method
        )
        db.session.add(payment)
        
        order.status = 'completed'
        db.session.commit()
        
        return payment, None