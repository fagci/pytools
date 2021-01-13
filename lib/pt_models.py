"""Database models to use with python tools"""
from datetime import datetime
from flask.helpers import url_for

from peewee import BooleanField, DateTimeField, ForeignKeyField, IntegerField, Model, SqliteDatabase, TextField
from playhouse.mysql_ext import JSONField
from flask_admin.contrib.peewee.filters import FilterEqual
from markupsafe import Markup

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


class SEOSession(BaseModel):
    """Runs of SEO checker"""
    created_at = DateTimeField(default=datetime.now())
    base_url = TextField()
    options = JSONField(null=True)

    @property
    def view(self):
        return Markup('<a href="{}">GO!</a>'.format(url_for('seocheckresult.index_view')+'?flt1_session_id_equals=' + str(self.id)))

    _admin = {
        'can_edit': False,
        'can_create': False,
        'can_delete': False,
        'column_list': ('created_at', 'base_url', 'results', 'options', 'view'),
        'column_formatters': {
            'created_at': lambda v, c, m, p: m.created_at.strftime('%d.%m.%Y %H:%M:%S'),
            'results': lambda v, c, m, p: m.results.count(),
        },
    }


def _raw_formatter(v, c, m, p):
    return Markup('<pre><code>{}</code></pre>'.format(getattr(m, p)))


def _url_newlines_formatter(v, c, m, p):
    return Markup(m.url.replace('/', '/<br />'))


ICON_OK = '<i class="fa fa-check"></i>'
ICON_FAIL = '<i class="fa fa-close text-danger"></i>'
ICON_TITLE = '<div title="{}">{}</div>'


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

    _admin = {
        # flask-admin ModelView attributes
        'can_edit': False,
        'can_create': False,
        'can_delete': False,
        'can_view_details': True,
        'page_size': '250',
        'named_filter_urls': True,
        'column_exclude_list': ('code', 'created_at', 'id', 'validation', 'ttfb', 'code', 'title_len', 'desc_len'),
        'column_filters': [
            FilterEqual(column=SEOSession.id, name='Session ID')
        ],
        'column_labels': dict(code_ok='Cod', ttfb_ok='TTFB', title_ok='T_OK', desc_ok='D_OK', title_len='TL', desc_len='DL', session='Sess'),
        'column_formatters': {
            'created_at': lambda v, c, m, p: m.created_at.strftime('%H:%M:%S'),
            'url': _url_newlines_formatter,
            'ttfb_ok': lambda v, c, m, p: Markup(ICON_TITLE.format(m.ttfb, ICON_OK if m.ttfb_ok else ICON_FAIL)),
            'code_ok': lambda v, c, m, p: Markup(ICON_TITLE.format(m.code, ICON_OK if m.code_ok else ICON_FAIL)),
            'title_ok': lambda v, c, m, p: Markup(ICON_TITLE.format(m.title_len, ICON_OK if m.title_ok else ICON_FAIL)),
            'desc_ok': lambda v, c, m, p: Markup(ICON_TITLE.format(m.desc_len, ICON_OK if m.desc_ok else ICON_FAIL)),
            'headings': _raw_formatter,
        },
    }


def create_tables():
    db.create_tables([FortuneIP, SEOSession, SEOCheckResult])
