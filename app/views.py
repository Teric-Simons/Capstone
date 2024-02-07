import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app.forms import LoginForm, RegisterForm
from flask import send_from_directory
db.create_all()
###
# Routing for your application.
###
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')






#----------------------------------------------------------------------------#



@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    """Render the website's sign up page"""
    form = RegisterForm()
    #stores new credentials to user table in database on submit
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        confirmPassword = form.confirmPassword.data

        sameEmail = User.query.filter_by(email=email).first()
        if sameEmail:
            flash('Email already exists', 'danger')
            return redirect(url_for('register'))

        if password != confirmPassword:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))
        
        user = User(email, password)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception:
            flash('Database Error', 'danger')
            return redirect(url_for('home'))

        flash('Registration Successful! You may now proceed to Log In.', 'success')            
        return redirect(url_for('login'))
    else:
        flash_errors(form)        
    return render_template('register.html', form = form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Get the username and password values from the form.
        email = form.email.data
        password = form.password.data

     
        user = User.query.filter_by(email=email).first()

        if user is None or not check_password_hash(user.password, password):
            flash('Incorrect login information', 'danger')
            return redirect(url_for('login'))
        
        
        # Gets user id, load into session
        login_user(user)

        flash('You have succesfully logged in.', 'success')
        return redirect(url_for("login"))  # The user should be redirected to the upload form instead
    return render_template("login.html", form=form)


# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(User).filter_by(id=id)).scalar()



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Success')
    return redirect(url_for('home'))






@app.route('/chat')
def chat():
    return render_template("chat.html")


