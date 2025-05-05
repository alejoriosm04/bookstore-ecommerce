from extensions import db

class DeliveryProvider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    coverage_area = db.Column(db.String(150))
    cost = db.Column(db.Float)