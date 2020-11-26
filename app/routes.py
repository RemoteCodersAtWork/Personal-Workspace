from flask import render_template , flash , redirect , url_for , request
from app import app
from app.forms import RegisterForm , LoginForm
from app.models import User
from app import app, db, password
from flask_login import login_user , current_user , logout_user , login_required

@app.route('/')

def homepage():

    return render_template("information.html")

@app.route("/register" , methods=['GET','POST'])
def registerpage():

    if current_user.is_authenticated:

        flash("You are already logged in." , "warning")
        return redirect(url_for("homepage"))

    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():

        hashed = password.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data , email=form.email.data , password=hashed)
        
        db.session.add(user)
        db.session.commit()

        flash("Account created for %s!" % (form.username.data) , "success")
        return redirect(url_for("loginpage"))

    return render_template("register.html" , form=form)

@app.route("/login" , methods=['GET','POST'])
def loginpage():

    if current_user.is_authenticated:

        flash("You are already logged in." , "warning")
        return redirect(url_for("homepage"))

    form = LoginForm(request.form)

    if request.method == "POST" and form.validate():

        member = User.query.filter_by(username = form.username.data).first()

        if member and password.check_password_hash(member.password , form.password.data):
            login_user(member)
            flash("Welcome, %s!" % (form.username.data) , "success")
            return redirect(url_for("homepage"))

        else:
            flash("Username or Password doesn't match, please try again." , "danger")
            return redirect(url_for("loginpage"))

    return render_template("login.html" , form=form)

@app.route("/logout")
def logoutpage():

    logout_user()

    flash("Successfuly logged out." , "success")
    return redirect(url_for("homepage"))

@app.route("/member-page")
@login_required

def member():
    return render_template("members.html")