# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm as Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, SelectField, PasswordField # BooleanField

# Import Form validators
from wtforms.validators import Required, Email, EqualTo, Length


# Define the login form (WTForms)

class UserForm(Form):
    email = TextField('Email Address', [Email(),
                Required(message='Forgot your email address?')])
    name = TextField('Nombre', [Length(max=10),
                Required(message='Forgot your Password?')])
    password = TextField('Password', [Length(max=10),
                Required(message='Forgot your Password?')])


class LoginForm(Form):
    email = TextField('Email Address', [Email(),
                Required(message='Forgot your email address?')])
    password = TextField('Password', [Length(max=10),
                Required(message='Forgot your Password?')])