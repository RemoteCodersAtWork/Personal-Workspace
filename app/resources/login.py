from flask import render_template , flash , redirect , url_for , request
from app.forms import LoginForm
from app.models import User
from app import app, db, password
from flask_login import login_user , current_user , logout_user , login_required

@app.route("/login" , methods=['GET','POST'])
def loginpage():

    if current_user.is_authenticated:
        return redirect(url_for("homepage"))

    form = LoginForm(request.form)

    if request.method == "POST" and form.validate():

        member = User.query.filter_by(email = form.email.data).first()

        if member and password.check_password_hash(member.password , form.password.data):
            login_user(member)
            return redirect(url_for("homepage"))

        else:
            flash("Email or Password doesn't match, please try again." , "errlable")
            return redirect(url_for("loginpage"))

    return render_template("login.html" , form=form)

@app.route("/logout")
def logoutpage():

    logout_user()

    flash("Successfuly logged out." , "successlable")
    return redirect(url_for("loginpage"))

@app.route("/member-page")
@login_required
def member():
    return render_template("members.html")