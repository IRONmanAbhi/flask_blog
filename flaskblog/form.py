from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User, Posts


class registrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirmPass = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")]) # name of qualto validator variable must be passed as a string
    submit = SubmitField("Sign Up")
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if(user):
            raise ValidationError("This Username is taken. Please choose another username")
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if(user):
            raise ValidationError("Account associated with this email already exists.")
    
    
class loginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Sign In")