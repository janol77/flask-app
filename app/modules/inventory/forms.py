# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm as Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, SelectField, PasswordField # BooleanField

# Import Form validators
from wtforms.validators import Required, Email, EqualTo, Length


# Define the login form (WTForms)

class InventoryForm(Form):
    optico = TextField('Optico', [Required(message='Debe ingresar nombre del optico')])
    tipo = SelectField('uno', choices=['uno','dos','tres'], coerce=unicode)
    ean = TextField('Codigo de barra', [Length(max=10),
                Required(message='Debe ingresar el codigo de barra')])