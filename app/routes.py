from flask import render_template , redirect , url_for
from app.models import User
from app import app
from flask_login import login_user , current_user

@app.route('/')
def homepage():

    if current_user.is_authenticated:
        return render_template("members.html")
    else:
        return render_template("information.html")