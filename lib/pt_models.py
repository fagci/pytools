"""Database models to use with python tools"""
import pymorphy2
from datetime import datetime

from peewee import BooleanField, CharField, DateTimeField, ForeignKeyField, IntegerField, Model, SqliteDatabase, TextField
from playhouse.mysql_ext import JSONField

db = SqliteDatabase('db.sqlite3')


class BaseModel(Model):
    """Base model to use database"""
    class Meta:
        database = db

# Create user model.


class User(BaseModel):
    first_name = CharField(100, null=True)
    last_name = CharField(100, null=True)
    login = CharField(80, unique=True)
    email = CharField(120)
    password = CharField(64)
    is_admin = BooleanField(default=False)

    def get_id(self):
        return self.id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    # Required for administrative interface
    def __unicode__(self):
        return '{} {} <{}>'.format(self.first_name, self.last_name, self.email)


class FortuneIP(BaseModel):
    """Storage of gathered IPs"""
    created_at = DateTimeField(default=datetime.now())
    ip = TextField()
    port = IntegerField()
    title = TextField(null=True)
    description = TextField(null=True)


class SEOSession(BaseModel):
    """Runs of SEO checker"""
    created_at = DateTimeField(default=datetime.now())
    base_url = TextField()
    options = JSONField(null=True)

    @property
    def view(self):
        from flask import Markup
        from flask.helpers import url_for
        return Markup('<a href="{}">GO!</a>'.format(url_for('seocheckresult.index_view')+'?flt1_session_id_equals=' + str(self.id)))


morph = pymorphy2.MorphAnalyzer()


class SEOCheckResult(BaseModel):
    """One url results of SEO check session"""
    session = ForeignKeyField(model=SEOSession, backref='results')
    created_at = DateTimeField(default=datetime.now())
    url = TextField()
    code_ok = BooleanField()
    code = IntegerField()
    ttfb_ok = BooleanField()
    ttfb = IntegerField()
    title_ok = BooleanField()
    title_len = IntegerField()
    title_text = TextField()
    desc_ok = BooleanField()
    desc_len = IntegerField()
    desc_text = TextField()
    headings = TextField()
    validation = TextField()
    comment = TextField()

    @property
    def words(self):
        from collections import Counter
        import re
        from stop_words import get_stop_words
        from markupsafe import Markup

        # todo: fix by lang preference
        stop_words = get_stop_words('ru') + get_stop_words('en')
        title_lemmas = []
        string = '{} {}'.format(self.title_text, self.desc_text).lower()
        words = re.findall(r'\w+', string)

        for word in words:
            if word in stop_words:
                continue
            lemmas = morph.parse(word)
            if lemmas:
                title_lemmas.append(lemmas[0].normal_form)
        counts = Counter(title_lemmas)

        return Markup('<br />'.join(['{}: {}'.format(k, v) for k, v in counts.items() if v > 1]))


def create_tables():
    db.create_tables([User, FortuneIP, SEOSession, SEOCheckResult])
