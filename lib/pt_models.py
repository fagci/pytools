"""Database models to use with python tools"""
from datetime import datetime

from peewee import DateTimeField, Model, SqliteDatabase, TextField

db = SqliteDatabase('db.sqlite3')


class BaseModel(Model):
    """Base model to use database"""
    class Meta:
        database = db


class Fortune(BaseModel):
    """Model to store IPs with http server home page titles"""
    created_at = DateTimeField(default=datetime.now())
    ip = TextField(primary_key=True)
    title = TextField()


def create_tables():
    db.create_tables([Fortune])
