class Admin():
    def __init__(self, modules):
        self._modules = modules

    def run(self, host='127.0.0.1', port=8888, user='admin', password='ptpass'):
        """Runs web interface"""
        from inspect import isclass
        import secrets

        from flask import Flask, cli, render_template
        from flask_admin import Admin, expose, AdminIndexView
        from flask_admin.contrib.peewee import ModelView
        from flask_basicauth import BasicAuth
        from flask_admin.base import BaseView

        import lib.pt_models as models

        cli.show_server_banner = lambda *_: None

        app = Flask(__name__, template_folder='../templates')
        app.config['BASIC_AUTH_USERNAME'] = user
        app.config['BASIC_AUTH_PASSWORD'] = password
        secret_key = secrets.token_hex(16)
        app.config['SECRET_KEY'] = secret_key

        basic_auth = BasicAuth(app)

        modules = self._modules

        class IndexView(AdminIndexView):
            @expose('/')
            @basic_auth.required
            def index(self):
                return self.render('admin/index.html', modules=modules)

        class ModuleView(BaseView):
            @expose('/')
            @basic_auth.required
            def index(self):
                return self.render('admin/module.html', modules=modules)

        class PTModelView(ModelView):
            @basic_auth.required
            def is_accessible(self):
                return super().is_accessible()

        admin = Admin(app, 'PyTools admin',
                      template_mode='bootstrap4', index_view=IndexView(), base_template='admin/base.html')

        @app.route('/')
        def index():
            return render_template('index.html')

        for member in models.__dict__:
            if member.startswith('_'):
                continue
            m = getattr(models, member)
            if isclass(m) and m is not models.BaseModel and issubclass(m, models.BaseModel):
                admin.add_view(PTModelView(m))

        try:
            import local.models as local_models

            for member in local_models.__dict__:
                if member.startswith('_'):
                    continue
                m = getattr(local_models, member)
                if isclass(m) and m is not local_models.BaseModel and issubclass(m, local_models.BaseModel):
                    admin.add_view(PTModelView(m))
        except:
            pass

        for m in modules:
            admin.add_view(ModuleView(m, 'modules', 'admin.' + m))

        app.run(host, port)
