from datetime import datetime

from peewee import DateTimeField, Model, SqliteDatabase, TextField

db = SqliteDatabase('db.sqlite3')


class BaseModel(Model):
    class Meta:
        database = db


class Fortune(BaseModel):
    created_at = DateTimeField(default=datetime.now())
    ip = TextField(primary_key=True)
    title = TextField()


def create_tables():
    db.create_tables([Fortune])
