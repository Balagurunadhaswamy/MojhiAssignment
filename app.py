# -*- coding: utf-8 -*-
"""
Main module/app file for login and logout, That stores
the user session until logged out created using 
Python, Flask and MongoDb with HTML, CSS and Bootstrap
for the frontend and JS and Ajax for funtionality.
"""

from flask import Flask, render_template, redirect, session
from functools import wraps
from user.models import User

app = Flask(__name__)
app.secret_key = b'\xa6\xb5\x7f\xf7\x8b\xf1t\xe2ZQC;J\xfa\xe9\xfa'

"""
Development environment which restarts the 
app every time a change is made in the app.
"""

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True


@app.route('/user/signup', methods=['POST'])
def signup():
    """
    Function for user to create an account
    Input : Form data sent via POST
    Output : success 200, user information in dictionary format
    """
    return User().signup()

@app.route('/user/signout')
def signout():
    """
    Function for user log out of a session
    Input : Clicking on logout button
    Output : Redirected to the login page.
    """
    return User().signout()

@app.route('/user/login', methods=['POST'])
def login():
    """
    Function for user to login in to the dashboard
    Input : Email and password of the user.
    Output : Redirected to the dashboard that conntains
    the information of the logged in user.
    """
    return User().login()

# Starts session once logged in.

def login_required(f):
    """
    Function to prevent user from accessing the 
        dashboard without logging in
    Input : Login credentials of the user
    Output : If the user is logged in then the
        user can access the dashboard else the user
        will be redirected to the login page
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    
    return wrap

# Route to the main page.

@app.route('/')
def loginform():
    """
    Opening page of the app.
    User can either login in to the dashboard or
        go on tpo create a new account
    """
    return render_template('login.html')

# Route to create account.

@app.route('/create/')
def home():
    """
    Page to create New Account
    Input: Name, Email and password
    Output: Redirected if the credentials or valid, If not 
        error message appears
    """
    return render_template('home.html')

# Route to dashboard. Dashboard cannot be accessed without logging in.

@app.route('/dashboard/')
@login_required
def dashboard():
    """
    Dashboard page that lets logged in 
        user to view their info
    Input : Giving in the correct credentials
        in the login page
    Output : Viewing the dashboard.
    """
    return render_template('dashboard.html')
