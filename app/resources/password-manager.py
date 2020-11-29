from flask import render_template , flash , redirect , url_for , request
from app.forms import LoginForm
from app.models import User
from app import app, db, password
from flask_login import login_user , current_user , logout_user , login_required

@app.route("/password-manager" , methods=['GET','POST'])
def passwordmanagerpage():
    