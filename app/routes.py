from flask import render_template , flash , redirect , url_for , request
from app import app
from app.forms import RegisterForm , LoginForm
from app.models import User
from app import app, db, password
from flask_login import login_user , current_user , logout_user , login_required
from threading import Thread
from flask_mail import Mail, Message

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
        user = User(fname=form.fname.data ,lname=form.lname.data , email=form.email.data , password=hashed)
        
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

        member = User.query.filter_by(email = form.email.data).first()

        if member and password.check_password_hash(member.password , form.password.data):
            login_user(member)
            flash("Welcome, %s" % (form.fname.data), " %s!" % (form.lname.data), "success")
            return redirect(url_for("homepage"))

        else:
            flash("Email or Password doesn't match, please try again." , "danger")
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


@app.route("/forgotpassword" , methods=['GET','POST'])
def forgotpasswordpage():

    form = ForgotPasswordForm(request.form)

    if request.method == "POST" and form.validate():

        member = User.query.filter_by(email = form.email.data).first()

        if member and password.check_password_hash(member.password , form.password.data):
            login_user(member)
            flash("Welcome, %s" % (form.fname.data), " %s!" % (form.lname.data), "success")
            return redirect(url_for("homepage"))

        else:
            flash("Email or Password doesn't match, please try again." , "danger")
            return redirect(url_for("loginpage"))

    return render_template("login.html" , form=form)

if request.method=="POST":
        mail = request.form['mail']
        check = User.query.filter_by(mail=mail).first()

        if check:
            def get_random_string(length=24,allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
                return ''.join(random.choice(allowed_chars) for i in range(length))
            hashCode = get_random_string()
            check.hashCode = hashCode
            db.session.commit()
            msg = Message('Confirm Password Change', sender = 'berat@github.com', recipients = [mail])
            msg.body = "Hello,\nWe've received a request to reset your password. If you want to reset your password, click the link below and enter your new password\n http://localhost:5000/" + check.hashCode
            posta.send(msg)
            return '''
                <form action="/" method="post">
                    <small>enter the email address of the account you forgot your password</small> <br>
                    <input type="email" name="mail" id="mail" placeholder="mail@mail.com"> <br>
                    <input type="submit" value="Submit">
                </form>
            '''
    else:
        return '''
            <form action="/" method="post">
                <small>enter the email address of the account you forgot your password</small> <br>
                <input type="email" name="mail" id="mail" placeholder="mail@mail.com"> <br>
                <input type="submit" value="Submit">
            </form>
        '''
    
@app.route("/<string:hashCode>",methods=["GET","POST"])
def hashcode(hashCode):
    check = User.query.filter_by(hashCode=hashCode).first()    
    if check:
        if request.method == 'POST':
            passw = request.form['passw']
            cpassw = request.form['cpassw']
            if passw == cpassw:
                check.password = passw
                check.hashCode= None
                db.session.commit()
                return redirect(url_for('index'))
            else:
                flash('yanlış girdin')
                return '''
                    <form method="post">
                        <small>enter your new password</small> <br>
                        <input type="password" name="passw" id="passw" placeholder="password"> <br>
                        <input type="password" name="cpassw" id="cpassw" placeholder="confirm password"> <br>
                        <input type="submit" value="Submit">
                    </form>
                '''
        else:
            return '''
                <form method="post">
                    <small>enter your new password</small> <br>
                    <input type="password" name="passw" id="passw" placeholder="password"> <br>
                    <input type="password" name="cpassw" id="cpassw" placeholder="confirm password"> <br>
                    <input type="submit" value="Submit">
                </form>
            '''
    else:
        return render_template('/')