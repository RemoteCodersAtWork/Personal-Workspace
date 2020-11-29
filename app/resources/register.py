from flask import render_template , flash , redirect , url_for , request
from app.forms import RegisterForm
from app.models import User
from app import app, db, password
from flask_login import current_user

@app.route("/register" , methods=['GET','POST'])
def registerpage():

    if current_user.is_authenticated:

        flash("You are already logged in." , "warninglable")
        return redirect(url_for("homepage"))

    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():

        hashed = password.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fname=form.fname.data ,lname=form.lname.data , email=form.email.data , password=hashed)
        
        db.session.add(user)
        db.session.commit()

        flash("Account created for %s!" % (form.fname.data) , "successlable")
        return redirect(url_for("loginpage"))

    return render_template("register.html" , form=form)