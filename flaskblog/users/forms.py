from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user


class registrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirmPass = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")]) # name of equalto validator variable must be passed as a string
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
    
    
class accountUpdateForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField("Update Profile Picture", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Update")
    
    def validate_username(self, username):
        if(username.data != current_user.username):
            user = User.query.filter_by(username=username.data).first()
            if(user):
                raise ValidationError("This Username is taken. Please choose another username")
        
    def validate_email(self, email):
        if(email.data != current_user.email):
            user = User.query.filter_by(email=email.data).first()
            if(user):
                raise ValidationError("Account associated with this email already exists.")
            
class requestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Reset Password")
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if(user is None):
            raise ValidationError("No Account is associated with this email!")
    

class resetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirmPass = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")]) # name of qualto validator variable must be passed as a string
    submit = SubmitField("Reset Password")