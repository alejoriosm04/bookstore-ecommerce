from flask import Blueprint, render_template, request, redirect, url_for
from models.payment import Payment
from models.purchase import Purchase
from extensions import db
#from app import db
from flask_login import login_required

payment = Blueprint('payment', __name__)

@payment.route('/payment/<int:purchase_id>', methods=['GET', 'POST'])
@login_required
def payment_page(purchase_id):
    if request.method == 'POST':
        method = request.form.get('method')
        new_payment = Payment(purchase_id=purchase_id, amount=request.form.get('amount'), payment_method=method, payment_status='Paid')
        db.session.add(new_payment)
        purchase = Purchase.query.get(purchase_id)
        purchase.status = 'Paid'
        db.session.commit()
        return redirect(url_for('delivery.select_delivery', purchase_id=purchase_id))
    return render_template('payment.html', purchase_id=purchase_id)