class Admin():
    def __init__(self, modules):
        self._modules = modules

    def run(self, host='127.0.0.1', port=8888, user='admin', password='ptpass'):
        """Runs web interface"""

        self._init_flask()

        print('[*] Init admin...')

        self._app.config['BASIC_AUTH_USERNAME'] = user
        self._app.config['BASIC_AUTH_PASSWORD'] = password
        self._app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'

        self._load_models()
        self._load_modules()

        print('[*] Running server...')
        self._app.run(host, port)

    def _init_flask(self):
        print('[*] Init flask...')
        import secrets
        from flask import Flask, cli, render_template
        from flask_basicauth import BasicAuth
        from flask_admin import Admin, expose, AdminIndexView

        self._app = Flask(__name__, template_folder='../templates')
        cli.show_server_banner = lambda *_: None
        secret_key = secrets.token_hex(16)
        self._app.config['SECRET_KEY'] = secret_key
        self._basic_auth = BasicAuth(self._app)
        modules = self._modules

        @self._app.route('/')
        def index():
            return render_template('index.html')

        class IndexView(AdminIndexView):
            @expose('/')
            @self._basic_auth.required
            def index(self):
                return self.render('admin/index.html', modules=modules)
        self._admin = Admin(self._app, 'PyTools admin',
                            template_mode='bootstrap4', index_view=IndexView(), base_template='layout.html')

    def _load_modules(self):
        print('[*] Load modules...')
        from flask_admin import expose
        from flask_admin.base import BaseView

        modules = self._modules

        class ModuleView(BaseView):
            @expose('/')
            @self._basic_auth.required
            def index(self):
                return self.render('admin/module.html', modules=modules)

        for m in modules:
            self._admin.add_view(ModuleView(m, 'Modules', 'admin.' + m))

    def _load_models(self):
        print('[*] Load models...')
        import lib.pt_models as models
        self._load_models_from_module(models)

        try:
            import local.models as local_models
            self._load_models_from_module(local_models)
        except:
            pass

    def _load_models_from_module(self, module):
        print('[*] Load model {}...'.format(module.__name__))
        from inspect import isclass
        from flask_admin.contrib.peewee import ModelView

        class PTModelView(ModelView):
            def __init__(self, *args, **kwargs):
                model = args[0]
                kw = model._admin if hasattr(model, '_admin') else None
                if kw:
                    for k, v in kw.items():
                        setattr(self, k, v)
                super().__init__(*args, **kwargs)

            @self._basic_auth.required
            def is_accessible(self):
                return super().is_accessible()

        for member in module.__dict__:
            if member.startswith('_'):
                continue
            m = getattr(module, member)
            if isclass(m) and m is not module.BaseModel and issubclass(m, module.BaseModel):
                self._admin.add_view(PTModelView(m, category='Models'))
