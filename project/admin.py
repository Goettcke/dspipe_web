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

    print(email)
    print(name)
    print(password)
    print(user_type)

    user = User.query.filter_by(email=email).first()
    print(user)
    if user:  # if the user exists we redirect back to signup page, so user can login
        print(f"User {user} already exists")
        flash('Account already exists - try logging in')
        render_template("example_profile_page.html", name='Account already exists - try logging in') # Maybe this works
        print(f"User {user} already exists")
    else:
        print("User doesn't exist - let's create him")
        new_user = User(email=email, name=name, user_type=user_type, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for('main.admin_panel'))


@admin.route('/update_user_type', methods=['POST'])
@login_required
def update_user_type():
    # Code to validate and add user to database
    email = request.form.get('user_email')
    user_type = request.form.get('user_type')
    print(email)
    print(user_type)
    user = User.query.filter_by(email=email).first()

    if user:  # if the user exists we redirect back to signup page, so user can login
        user.user_type = user_type
        db.session.commit()
        return redirect(url_for('main.admin_panel'))
    else:
       return render_template("example_profile_page.html", name='Account already exists - try logging in') # Maybe this works

@admin.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    # Code to validate and add user to database
    email = request.form.get('user_email')
    user = User.query.filter_by(email=email).first()

    if user: # if the user exists we redirect back to signup page, so user can login
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('main.admin_panel'))
    else:
        return render_template("example_profile_page.html", name="Couldn't delete user - try logging in") # Maybe this works
