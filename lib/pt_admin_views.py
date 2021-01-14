from flask import Markup, redirect, request, url_for
from flask_admin import AdminIndexView, expose, helpers
from flask_admin.contrib.peewee import ModelView
from flask_admin.contrib.peewee.filters import FilterEqual
import flask_login as login

from lib.pt_models import SEOSession


def _raw_formatter(v, c, m, p):
    return Markup('<pre><code>{}</code></pre>'.format(getattr(m, p)))


def _url_newlines_formatter(v, c, m, p):
    return Markup(m.url.replace('/', '/<br />'))


ICON_OK = '<i class="fa fa-check"></i>'
ICON_FAIL = '<i class="fa fa-close text-danger"></i>'
ICON_TITLE = '<div title="{}">{}</div>'


class IndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(IndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        from lib.pt_admin_forms import LoginForm
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            login.login_user(form.get_user(), remember=True)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))

        self._template_args['form'] = form
        return super(IndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


class PTModelView(ModelView):
    def __init__(self, *args, **kwargs):
        model = args[0]
        kw = model._admin if hasattr(model, '_admin') else None
        if kw:
            for k, v in kw.items():
                setattr(self, k, v)
        super().__init__(*args, **kwargs)

    def is_accessible(self):
        import flask_login as login
        return login.current_user.is_authenticated


class UserView(PTModelView):
    def is_accessible(self):
        import flask_login as login
        from lib.pt_models import User  # todo: rm linkage
        print(login.current_user.is_admin)
        return super().is_accessible()


class SEOSessionView(PTModelView):
    can_edit = False
    can_create = False
    can_delete = False
    column_list = ('created_at', 'base_url', 'results', 'options', 'view')
    column_formatters = dict(
        created_at=lambda v, c, m, p: m.created_at.strftime(
            '%d.%m.%Y %H:%M:%S'),
        results=lambda v, c, m, p: m.results.count(),
    )


class SEOCheckResultView(PTModelView):
    # flask-admin ModelView attributes
    can_edit = True
    # edit_modal = True
    can_create = False
    can_delete = False
    can_view_details = True
    page_size = '250'
    named_filter_urls = True
    column_editable_list = ('comment',)
    column_list = (
        'url',
        'code_ok',
        'code',
        'ttfb_ok',
        'ttfb',
        'title_ok',
        'title_len',
        'title_text',
        'desc_ok',
        'desc_len',
        'desc_text',
        'headings',
        'validation',
        'comment',
        'words',
    )
    column_exclude_list = ('code', 'created_at', 'id',
                           'validation', 'ttfb', 'code', 'title_len', 'desc_len')
    column_filters = [
        FilterEqual(column=SEOSession.id, name='Session ID')
    ]
    column_labels = dict(code_ok='Cod', ttfb_ok='TTFB', title_ok='T_OK',
                         desc_ok='D_OK', title_len='TL', desc_len='DL', session='Sess')
    column_formatters = dict(
        created_at=lambda v, c, m, p: m.created_at.strftime('%H:%M:%S'),
        url=_url_newlines_formatter,
        ttfb_ok=lambda v, c, m, p: Markup(ICON_TITLE.format(
            m.ttfb, ICON_OK if m.ttfb_ok else ICON_FAIL)),
        code_ok=lambda v, c, m, p: Markup(ICON_TITLE.format(
            m.code, ICON_OK if m.code_ok else ICON_FAIL)),
        title_ok=lambda v, c, m, p: Markup(ICON_TITLE.format(
            m.title_len, ICON_OK if m.title_ok else ICON_FAIL)),
        desc_ok=lambda v, c, m, p: Markup(ICON_TITLE.format(
            m.desc_len, ICON_OK if m.desc_ok else ICON_FAIL)),
        headings=_raw_formatter,
    )
