from wtforms import Form , StringField , PasswordField , SubmitField , validators
from app.models import User

class RegisterForm(Form) :
    fname = StringField("Firstname" , validators=[validators.DataRequired() ,validators.Length(min=2 , message = "Firstname must be at least 2 characters long.")])
    lname = StringField("Lastname" , validators=[validators.DataRequired() ,validators.Length(min=2 , message = "Lastname must be at least 2 characters long.")])
    email = StringField("E-Mail" , validators=[validators.DataRequired() ,validators.Email() ,validators.Length(min=6 , message = "Email Address must be at least 6 characters long.")])
    password = PasswordField("Password" , validators=[validators.DataRequired() ,validators.Length(min=6 , message = "Password must be at least 6 characters long.")])
    confirm = PasswordField("Confirm Password" , validators=[validators.EqualTo('password' , message = "Passwords do not match.") ,validators.DataRequired()])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise validators.ValidationError("Username already exists.")
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise validators.ValidationError("Email already exists.")

class LoginForm(Form) :
    email = StringField("E-Mail", validators=[validators.DataRequired() ,validators.Length(min=6 , max=30)])
    password = PasswordField("Password", validators=[validators.DataRequired() , validators.Length(min=6 , max=20)])
    submit = SubmitField("Login")