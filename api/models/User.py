from .base import db, DBUtil
from .UserMazes import UserMazes
from api.core import Mixin
from sqlalchemy.orm import relationship


# Note that we use sqlite for our tests, so you can't use Postgres Arrays
class User(Mixin, DBUtil, db.Model):
    """User Table."""

    __tablename__ = "user"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.username}; {'*' * len(self.password)}>"
