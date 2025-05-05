from extensions import db

class DeliveryAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'))
    provider_id = db.Column(db.Integer, db.ForeignKey('delivery_provider.id'))
