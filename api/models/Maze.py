from .base import db, DBUtil
from .UserMazes import UserMazes
from api.core import Mixin
from sqlalchemy.orm import relationship


class Maze(Mixin, DBUtil, db.Model):
    """Mazes Table."""

    __tablename__ = "maze"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    entrance = db.Column(db.String, nullable=False)
    grid = db.Column(db.String, nullable=False)
    walls = db.Column(db.String, nullable=False)
    min_path = db.Column(db.String)
    max_path = db.Column(db.String)
    #children = relationship(UserMazes, cascade="all,delete", backref="parent")

    def __init__(self, entrance, grid, walls, min_path, max_path, calories_limit=2100):
        self.entrance = entrance
        self.grid = grid
        self.walls = walls
        self.min_path = min_path
        self.max_path = max_path

    def __repr__(self):
        return f"<Maze {self.entrance}; {self.grid}; {self.grid}>"
