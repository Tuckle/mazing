from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import ClauseElement

db = SQLAlchemy()


class DBUtil:
    @classmethod
    def get_or_create(cls, obj, defaults=None, **kwargs):
        instance = db.session.query(obj).filter_by(**kwargs).one_or_none()
        if instance:
            return instance, False
        else:
            params = {k: v for k, v in kwargs.items() if not isinstance(v, ClauseElement)}
            params.update(defaults or {})
            instance = obj(**params)
            try:
                db.session.add(instance)
                db.session.commit()
            except Exception:
                db.session.rollback()
                instance = db.session.query(obj).filter_by(**kwargs).one()
                return instance, False
            else:
                return instance, True
