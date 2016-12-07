from app import db


class User(db.Document):
    name = db.StringField(required=True)
    password = db.StringField(required=True)
    email = db.StringField(required=True)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
    	# import pdb;pdb.set_trace()
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id.__str__()

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
