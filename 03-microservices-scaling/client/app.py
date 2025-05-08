from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')
API_GATEWAY_URL = os.getenv('API_GATEWAY_URL', 'http://api-gateway:5000')

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('view_catalog'))

# Auth Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        response = requests.post(
            f"{API_GATEWAY_URL}/auth/login",
            json={
                'email': request.form['email'],
                'password': request.form['password']
            }
        )
        
        if response.status_code == 200:
            session['user'] = response.json()
            session['token'] = response.json()['token']
            flash('Login successful!', 'success')
            return redirect(url_for('view_catalog'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        response = requests.post(
            f"{API_GATEWAY_URL}/auth/register",
            json={
                'name': request.form['name'],
                'email': request.form['email'],
                'password': request.form['password']
            }
        )
        
        if response.status_code == 201:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Email may already exist.', 'danger')
    
    return render_template('auth/register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Book Routes
@app.route('/catalog')
def view_catalog():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    try:
        response = requests.get(
            f"{API_GATEWAY_URL}/books",
            headers={'Authorization': f"Bearer {session['token']}"}
        )
        
        if response.status_code == 200:
            books = response.json()
            return render_template('books/catalog.html', books=books)
        else:
            flash('Failed to load catalog.', 'danger')
            return render_template('books/catalog.html', books=[])
    
    except Exception as e:
        flash('Error connecting to service.', 'danger')
        return render_template('books/catalog.html', books=[])

@app.route('/my-books')
def my_books():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    try:
        response = requests.get(
            f"{API_GATEWAY_URL}/books",
            headers={'Authorization': f"Bearer {session['token']}"}
        )
        
        if response.status_code == 200:
            books = response.json()
            return render_template('books/my_books.html', books=books)
        else:
            flash('Failed to load your books.', 'danger')
            return render_template('books/my_books.html', books=[])
    
    except Exception as e:
        flash('Error connecting to service.', 'danger')
        return render_template('books/my_books.html', books=[])

@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            response = requests.post(
                f"{API_GATEWAY_URL}/books",
                json={
                    'title': request.form['title'],
                    'author': request.form['author'],
                    'description': request.form['description'],
                    'price': float(request.form['price']),
                    'stock': int(request.form['stock']),
                    'seller_id': session['user']['user_id']
                },
                headers={'Authorization': f"Bearer {session['token']}"}
            )
            
            if response.status_code == 201:
                flash('Book added successfully!', 'success')
                return redirect(url_for('my_books'))
            else:
                flash('Failed to add book.', 'danger')
        
        except Exception as e:
            flash('Error connecting to service.', 'danger')
    
    return render_template('books/add_book.html')

@app.route('/edit-book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            response = requests.put(
                f"{API_GATEWAY_URL}/books/{book_id}",
                json={
                    'title': request.form['title'],
                    'author': request.form['author'],
                    'description': request.form['description'],
                    'price': float(request.form['price']),
                    'stock': int(request.form['stock'])
                },
                headers={'Authorization': f"Bearer {session['token']}"}
            )
            
            if response.status_code == 200:
                flash('Book updated successfully!', 'success')
                return redirect(url_for('my_books'))
            else:
                flash('Failed to update book.', 'danger')
        
        except Exception as e:
            flash('Error connecting to service.', 'danger')
    
    # Get book details
    try:
        response = requests.get(
            f"{API_GATEWAY_URL}/books/{book_id}",
            headers={'Authorization': f"Bearer {session['token']}"}
        )
        
        if response.status_code == 200:
            book = response.json()
            return render_template('books/edit_book.html', book=book)
        else:
            flash('Book not found.', 'danger')
            return redirect(url_for('my_books'))
    
    except Exception as e:
        flash('Error connecting to service.', 'danger')
        return redirect(url_for('my_books'))

@app.route('/delete-book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    try:
        response = requests.delete(
            f"{API_GATEWAY_URL}/books/{book_id}",
            headers={'Authorization': f"Bearer {session['token']}"}
        )
        
        if response.status_code == 200:
            flash('Book deleted successfully!', 'success')
        else:
            flash('Failed to delete book.', 'danger')
    
    except Exception as e:
        flash('Error connecting to service.', 'danger')
    
    return redirect(url_for('my_books'))

# Order Routes
@app.route('/checkout/<int:book_id>', methods=['GET', 'POST'])
def checkout(book_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            response = requests.post(
                f"{API_GATEWAY_URL}/orders",
                json={
                    'user_id': session['user']['user_id'],
                    'book_id': book_id,
                    'quantity': int(request.form['quantity'])
                },
                headers={'Authorization': f"Bearer {session['token']}"}
            )
            
            if response.status_code == 201:
                order = response.json()
                return redirect(url_for('payment', order_id=order['id']))
            else:
                flash('Failed to create order.', 'danger')
        
        except Exception as e:
            flash('Error connecting to service.', 'danger')
    
    # Get book details
    try:
        response = requests.get(
            f"{API_GATEWAY_URL}/books/{book_id}",
            headers={'Authorization': f"Bearer {session['token']}"}
        )
        
        if response.status_code == 200:
            book = response.json()
            return render_template('orders/checkout.html', book=book)
        else:
            flash('Book not found.', 'danger')
            return redirect(url_for('view_catalog'))
    
    except Exception as e:
        flash('Error connecting to service.', 'danger')
        return redirect(url_for('view_catalog'))

@app.route('/payment/<int:order_id>', methods=['GET', 'POST'])
def payment(order_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            response = requests.post(
                f"{API_GATEWAY_URL}/orders/{order_id}/pay",
                json={
                    'method': request.form['payment_method']
                },
                headers={'Authorization': f"Bearer {session['token']}"}
            )
            
            if response.status_code == 200:
                return redirect(url_for('order_confirmation', order_id=order_id))
            else:
                flash('Payment failed. Please try again.', 'danger')
        
        except Exception as e:
            flash('Error processing payment.', 'danger')
    
    return render_template('orders/payment.html', order_id=order_id)

@app.route('/order-confirmation/<int:order_id>')
def order_confirmation(order_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    return render_template('orders/order_confirmation.html', order_id=order_id)

@app.route('/users')
def list_users():
    response = requests.get(
        f"{API_GATEWAY_URL}/users",
        headers={'Authorization': f"Bearer {session.get('token')}"}
    )
    users = response.json()
    return render_template('auth/list.html', users=users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)