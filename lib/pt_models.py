"""Database models to use with python tools"""
from datetime import datetime

from peewee import DateTimeField, IntegerField, Model, SqliteDatabase, TextField

db = SqliteDatabase('db.sqlite3')


class BaseModel(Model):
    """Base model to use database"""
    class Meta:
        database = db


class FortuneIP(BaseModel):
    """Storage of gathered IPs"""
    created_at = DateTimeField(default=datetime.now())
    ip = TextField()
    port = IntegerField()
    title = TextField(null=True)
    description = TextField(null=True)


def create_tables():
    db.create_tables([FortuneIP])
