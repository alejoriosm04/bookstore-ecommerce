from extensions import db

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'))
    amount = db.Column(db.Float)
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(50))