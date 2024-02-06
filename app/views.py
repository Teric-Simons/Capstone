import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app.models import UserProfile
from app.forms import LoginForm, RegisterForm
from werkzeug.security import check_password_hash
from flask import send_from_directory


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









#----------------------------------------------------------------------------#



@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
     form = RegisterForm()
     return render_template('register.html', form = form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    
    # change this to actually validate the entire form submission
    # and not just one field
    if form.validate_on_submit():
        # Get the username and password values from the form.
        username = form.username.data
        password = form.password.data

        # Using your model, query database for a user based on the username
        # and password submitted. Remember you need to compare the password hash.
        # You will need to import the appropriate function to do so.
        # Then store the result of that query to a `user` variable so it can be
        # passed to the login_user() method below.
        user = UserProfile.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password, password):
            flash('Incorrect login information')
            return redirect(url_for('login'))
        

        
        # Gets user id, load into session
        login_user(user)


        # Remember to flash a message to the user
        flash('You have succesfully logged in.')
        return redirect(url_for("upload"))  # The user should be redirected to the upload form instead
    return render_template("login.html", form=form)


# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(UserProfile).filter_by(id=id)).scalar()



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Success')
    return redirect(url_for('home'))



@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    pass


