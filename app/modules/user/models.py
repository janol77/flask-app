from app.db import db
from werkzeug import generate_password_hash


class User(db.Document):
    name = db.StringField(required=True)
    password = db.StringField()
    email = db.StringField(required=True)
    deleted = db.BooleanField()

    def check_email(self, new_email):
        """Unique Email."""
        params = {'email': new_email,
                  'deleted': False}
        existing = self.__class__.objects.filter(**params).first()
        if existing:
            if self.id == existing.id:
                return True
            return False
        return True

    def generate_password(self):
        """Calculate the password."""
        self.password = generate_password_hash(self.password)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id.__str__()

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
