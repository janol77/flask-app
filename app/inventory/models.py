from app import db
import datetime


class Inventory(db.Document):
    optico = db.StringField(required=True)
    tipo = db.StringField(required=True)
    ean = db.StringField(required=True)