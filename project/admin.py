from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from werkzeug.security import generate_password_hash
from . import db
from .models import User

admin = Blueprint('admin', __name__)

@admin.route('/create_user', methods=['POST'])
@login_required
def create_user():
    # Code to validate and add user to database
    email = request.form.get('user_email')
    name = request.form.get('user_name')
    password = request.form.get('password')
    user_type = request.form.get('user_type')


    user = User.query.filter_by(email=email).first()

    if user:  # if the user exists we redirect back to signup page, so user can login
        flash('Account already exists - try logging in')
        return redirect(url_for('main.admin_panel'))
    try:

        new_user = User(email=email, name=name, user_type=user_type, password=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()
    except:
        flash('Please ensure all fields are filled out!')
        return redirect(url_for('main.admin_panel'))

    return redirect(url_for('main.admin_panel'))
