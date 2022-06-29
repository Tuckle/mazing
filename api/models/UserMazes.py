from sqlalchemy import PrimaryKeyConstraint, ForeignKeyConstraint

from .base import db, DBUtil
from api.core import Mixin


class UserMazes(Mixin, DBUtil, db.Model):
    """UserMazes Table."""

    __tablename__ = "usermazes"
    __table_args__ = (
        PrimaryKeyConstraint('user', 'maze', name='user_maze_pk'),
        # ForeignKeyConstraint(['user', 'maze'], ['user.id', 'maze.id'])
    )

    # id = db.Column(db.Integer, unique=True, primary_key=True)
    user = db.Column(
        db.Integer, db.ForeignKey("user.id")
    )
    maze = db.Column(
        db.Integer, db.ForeignKey("maze.id")
    )

    def __init__(self, user_id, maze_id):
        self.user = user_id
        self.maze = maze_id

    def __repr__(self):
        return f"<UserMaze {self.user}; {self.maze};>"
