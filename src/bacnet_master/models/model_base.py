from sqlalchemy import inspect

from src import db


class ModelBase(db.Model):
    __abstract__ = True

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        self.check_self()
        db.session.add(self)
        db.session.commit()

    def save_to_db_no_commit(self):
        self.check_self()
        db.session.add(self)

    @classmethod
    def commit(cls):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # Issue #85 filter_by(...).update(...) is not working in inheritance
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.check_self()
        db.session.commit()

    def check_self(self) -> (bool, any):
        return True

    def to_dict(self) -> dict:
        return {c.key: str(getattr(self, c.key))
                for c in inspect(self).mapper.column_attrs}
