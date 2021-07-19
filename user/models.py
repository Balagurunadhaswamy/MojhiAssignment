from os import name
import re
import uuid
import pymongo
from passlib.hash import pbkdf2_sha256

from flask import Flask, jsonify, request, session, redirect

from werkzeug.utils import redirect
from settings import HOST, PORT

client = pymongo.MongoClient(HOST, PORT)
db = client.user_login_system

class User:
    # Starts session to output the logged in user info.
    def start_session(self, user):
        """
        Function for user to create a session
        Input : logging in using the login form
        Output : Redirected to the dashboard if the session is true
            and the password is hidden.
        """
        del user['password']
        session['logged_in'] = True
        session['user'] = user 
        return jsonify(user), 200

    # Create the object user
    def signup(self):
        """
        Function for user to create an account while
            encrypting the password before storing in Db
            and validating the email.
        Input : Form data sent via POST
        Output : success 200, user information in dictionary format
        """
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }

        # Checking for existing email 
        if db.users.find_one({"email": user['email'] }):
            return jsonify({"error": "Email already exists"}), 400
        
        # Check if email is valid or not
        if not self.valid_email(user["email"]):
            return jsonify({"error": "Please enter a valid Email"}), 400
        
        # Check if password is valid or not
        if not self.valid_password(user["password"]):
            return jsonify({"error": "Please enter a valid Password"}), 400
        
        # Password encryption
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        # Insert user if no errors
        if db.users.insert_one(user):
            return self.start_session(user)

        # If the login fails for a diffrent reason this will give a message.

        return jsonify({"error": "Signup failed"}), 400 

    # Redirects user to "Login" page after clearing user session

    def signout(self):
        """
        Function for user to sign out of the session and dashboard
        Input : By clicking on the logout button
        Output : The current session will be cleared and 
            the user is redirected to the login form
        """
        session.clear()
        return redirect('/')

    # Logs in user if the provided email exists


    def login(self):
        """
        Function for user to log in to the user account after 
            the email check and password check
        Input : A form that contains the user email and correct
            pasword.
        Output : success 200, redirected to the dashboard.
        """
        user = db.users.find_one({
            "email": request.form.get('email')
        })
        
        # Checks if the provided password is correct or not. If not will give error saying "User not found"

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)

        # Throw error if the email does not exist in the DB or if the password is invalid.

        return jsonify({"error": "Invalid Credentials, Please try again"}), 401

    def valid_email(self, email):
        """
        Utility to check valid email
        """
        return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

    def valid_password(self, password):
        """
        Utility to check valid password
        """
        pass_reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        pat = re.compile(pass_reg)
        # searching regex                 
        mat = re.search(pat, password)
        return bool(mat)