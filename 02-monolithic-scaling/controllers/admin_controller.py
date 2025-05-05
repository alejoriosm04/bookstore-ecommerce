from flask import Blueprint, render_template
from models.user import User
from flask_login import login_required

admin = Blueprint('admin', __name__)

@admin.route('/admin/users')
@login_required
def list_users():
    users = User.query.all()
    return render_template('list_users.html', users=users)
