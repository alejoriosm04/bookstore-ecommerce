from flask import Flask, render_template
from extensions import db, login_manager
from models.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Luego importar blueprints
from controllers.auth_controller import auth
from controllers.book_controller import book
from controllers.purchase_controller import purchase
from controllers.payment_controller import payment
from controllers.delivery_controller import delivery
from controllers.admin_controller import admin

# Registrar blueprints
app.register_blueprint(auth)
app.register_blueprint(book, url_prefix='/book')
app.register_blueprint(purchase)
app.register_blueprint(payment)
app.register_blueprint(delivery)
app.register_blueprint(admin)

from models.delivery import DeliveryProvider

def initialize_delivery_providers():
    with app.app_context():
        if DeliveryProvider.query.count() == 0:
            providers = [
                DeliveryProvider(name="DHL", coverage_area="Internacional", cost=50.0),
                DeliveryProvider(name="FedEx", coverage_area="Internacional", cost=45.0),
                DeliveryProvider(name="Envia", coverage_area="Nacional", cost=20.0),
                DeliveryProvider(name="Servientrega", coverage_area="Nacional", cost=15.0),
            ]
            db.session.bulk_save_objects(providers)
            db.session.commit()

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
# OJO este conexto crea las tablas e inicia los proveedores de entrega, 
# se debe ejecutar cada que se reinstala y ejecuta la aplicación Bookstore
    with app.app_context():
        db.create_all()
        initialize_delivery_providers()
    app.run(host="0.0.0.0", debug=True)
