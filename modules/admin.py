class Admin():
    def __init__(self, modules):
        self._modules = modules

    def run(self, host='127.0.0.1', port=8888):
        """Runs web interface"""
        from lib.pt_models import create_tables

        create_tables()

        self._init_flask()
        self._init_login()

        self._init_admin()

        self._load_models()
        self._load_modules()

        print('[*] Running server...')
        self._app.run(host, port)

    def _init_flask(self):
        print('[*] Init flask...')
        import secrets
        from flask import Flask, cli, render_template

        self._app = Flask(__name__, template_folder='../templates')
        cli.show_server_banner = lambda *_: None
        secret_key = secrets.token_hex(16)
        self._app.config['SECRET_KEY'] = secret_key
        # Initialize flask-login

        modules = self._modules

        @self._app.route('/')
        def index():
            return render_template('index.html')

    def _init_login(self):
        print('[*] Init login...')
        import flask_login as login
        from lib.pt_models import User
        self._login_manager = login.LoginManager()
        self._login_manager.init_app(self._app)

        # Create user loader function
        @self._login_manager.user_loader
        def load_user(user_id):
            print('Check user {}'.format(user_id))
            return User.get(user_id)

    def _init_admin(self):
        print('[*] Init admin...')
        from flask import redirect, url_for, request
        from flask_admin import Admin, expose, AdminIndexView, helpers
        from werkzeug.security import generate_password_hash, check_password_hash
        from wtforms import form, fields, validators
        import flask_login as login
        from lib.pt_models import User

        if not User.select().where(User.login == 'ptadmin').exists():
            user = User()
            user.login = 'ptadmin'
            user.email = 'ptadmin@admin.adm'
            user.password = generate_password_hash('PT_p@$$w0rd')
            user.save()

        self._app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'

        # Create customized index view class that handles login & registration

        class IndexView(AdminIndexView):

            @expose('/')
            def index(self):
                if not login.current_user.is_authenticated:
                    return redirect(url_for('.login_view'))
                return super(IndexView, self).index()

            @expose('/login/', methods=('GET', 'POST'))
            def login_view(self):
                # handle user login
                form = LoginForm(request.form)
                if helpers.validate_form_on_submit(form):
                    user = form.get_user()
                    login.login_user(user, remember=True)

                if login.current_user.is_authenticated:
                    return redirect(url_for('.index'))
                # link = '<p>Don\'t have an account? <a href="' + \
                #     url_for('.register_view') + \
                #     '">Click here to register.</a></p>'
                self._template_args['form'] = form
                # self._template_args['link'] = link
                return super(IndexView, self).index()

            # @expose('/register/', methods=('GET', 'POST'))
            # def register_view(self):
            #     form = RegistrationForm(request.form)
            #     if helpers.validate_form_on_submit(form):
            #         user = User()

            #         form.populate_obj(user)

            #         user.password = generate_password_hash(form.password.data)

            #         user.save()

            #         login.login_user(user)
            #         return redirect(url_for('.index'))
            #     link = '<p>Already have an account? <a href="' + \
            #         url_for('.login_view') + '">Click here to log in.</a></p>'
            #     self._template_args['form'] = form
            #     self._template_args['link'] = link
            #     return super(IndexView, self).index()

            @expose('/logout/')
            def logout_view(self):
                login.logout_user()
                return redirect(url_for('.index'))

        # Define login and registration forms (for flask-login)
        class LoginForm(form.Form):
            login = fields.StringField(validators=[validators.required()])
            password = fields.PasswordField(validators=[validators.required()])

            def validate_login(self, field):
                user = self.get_user()

                if user is None:
                    raise validators.ValidationError('Invalid user')

                # we're comparing the plaintext pw with the the hash from the db
                if not check_password_hash(user.password, self.password.data):
                    # to compare plain text passwords use
                    # if user.password != self.password.data:
                    raise validators.ValidationError('Invalid password')

            def get_user(self):
                from lib.pt_models import User
                return User.select().where(User.login == self.login.data).first()

        class RegistrationForm(form.Form):
            login = fields.StringField(validators=[validators.required()])
            email = fields.StringField()
            password = fields.PasswordField(validators=[validators.required()])

            def validate_login(self, field):
                from lib.pt_models import User
                if User.select().where(User.login == self.login.data).count() > 0:
                    raise validators.ValidationError('Duplicate username')

        self._admin = Admin(self._app, 'PyTools admin',
                            template_mode='bootstrap4', index_view=IndexView(), base_template='layout.html')

    def _load_modules(self):
        print('[*] Load modules...')
        from flask_admin import expose
        from flask_admin.base import BaseView

        modules = self._modules

        class ModuleView(BaseView):
            @expose('/')
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

            def is_accessible(self):
                import flask_login as login
                return login.current_user.is_authenticated

        for member in module.__dict__:
            if member.startswith('_'):
                continue
            m = getattr(module, member)
            if isclass(m) and m is not module.BaseModel and issubclass(m, module.BaseModel):
                self._admin.add_view(PTModelView(m, category='Models'))
