"""SQLAlchemy models and utility functions for Sprint."""
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.String(25))
    value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'Record[id:{self.id},datetime{self.datetime},value{self.value}]'

