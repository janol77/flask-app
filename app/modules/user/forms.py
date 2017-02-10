# -*- coding: utf-8 -*-
# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm as Form
# , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField

# Import Form validators
from wtforms.validators import Required, Email, Length


# Define the login form (WTForms)

class UserForm(Form):
    email = TextField('Correo Electronico',
                      [Email(),
                       Required(message='Debe ingresar un correo electrónico')])
    name = TextField('Nombre',
                     [Length(max=25),
                      Required(message='Debe ingresar un Nombre')])
    password = PasswordField('Password',
                             [Length(max=8,
                                     min=6,
                                     message=u'La contraseña debe tener entre 6 y 8 carácteres'),
                              Required(message=u'Debe ingresar una contraseña válida')])


class LoginForm(Form):
    email = TextField('Email Address',
                      [Email(),
                       Required(message='Debe ingresar un correo electrónico')])
    password = PasswordField('Password',
                             [Length(max=8, min=6),
                              Required(message=u'Debe ingresar una contraseña válida')])
