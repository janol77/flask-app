# -*- coding: utf-8 -*-
# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm as Form
# , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, ValidationError

# Import Form validators
from wtforms.validators import Required, Email, Length, DataRequired, EqualTo


# Define the login form (WTForms)

# def password_check(form, field):
#     print field.data
#     size = len(field.data)
#     if size > 6 and size > 8:
#         raise ValidationError(u'La contraseña debe \
#          tener entre 6 y 8 carácteres')
#     if field.data != form.confirm.data:
#         raise ValidationError(u'Las contraseñas deben coincidir')


class UserForm(Form):
    email = TextField('Correo Electronico', [
        Email(),
        Required(message='Debe ingresar un correo electrónico')])
    name = TextField('Nombre',
                     [Length(max=25),
                      Required(message='Debe ingresar un Nombre')])
    password = PasswordField(u'Nueva Contraseña', [
        Length(max=8,
               min=6,
               message=u'La contraseña debe tener entre 6 y 8 carácteres'),
        DataRequired(message=u'Debe ingresar una contraseña válida'),
        EqualTo('confirm', message='Las contraseñas deben coincidir')])
    confirm = PasswordField(u'Repita Contraseña')


class EditUserForm(Form):
    email = TextField('Correo Electronico', [
        Email(),
        Required(message='Debe ingresar un correo electrónico')])
    name = TextField('Nombre',
                     [Length(max=25),
                      Required(message='Debe ingresar un Nombre')])
    password = PasswordField(u'Nueva Contraseña')
    confirm = PasswordField(u'Repita Contraseña')

    def validate_password(form, field):
        size = len(field.data)
        if size > 0:
            if size < 6 or size > 8:
                raise ValidationError(u'La contraseña debe \
                 tener entre 6 y 8 carácteres')
        if field.data != form.confirm.data:
            raise ValidationError(u'Las contraseñas deben coincidir')


class LoginForm(Form):
    email = TextField('Email Address', [
        Email(),
        Required(message='Debe ingresar un correo electrónico')])
    password = PasswordField('Password', [
        Length(max=8, min=6),
        DataRequired(message=u'Debe ingresar una contraseña válida')])
