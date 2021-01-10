"""Toolbox module loader"""


from flask_admin.base import BaseView


MODULES_DIR = 'modules'


class ToolframeLoader(object):
    """Load modules needed to fire up commands"""
    _modules = []

    def __init__(self):
        """Fill attributes to show as commands"""
        from pkgutil import iter_modules
        for module in iter_modules([MODULES_DIR]):
            if module.name.startswith('_'):
                continue
            self._modules.append(module.name)
            setattr(self, module.name, None)

    def commands(self):
        """List commands as tree"""
        self._command_tree(self)

    def admin(self, host='127.0.0.1', port=8888, user='admin', password='ptpass'):
        """Runs web interface"""
        from inspect import isclass

        from flask import Flask, cli, render_template
        from flask_admin import Admin, expose, AdminIndexView
        from flask_admin.contrib.peewee import ModelView
        from flask_basicauth import BasicAuth

        import lib.pt_models as models

        cli.show_server_banner = lambda *_: None

        app = Flask(__name__, template_folder='../templates')
        app.config['BASIC_AUTH_USERNAME'] = user
        app.config['BASIC_AUTH_PASSWORD'] = password

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
        for m in modules:
            admin.add_view(ModuleView(m, 'modules', 'admin.' + m))

        app.run(host, port)

    def _command_tree(self, c, level=0):
        from colorama import Fore
        colors = [Fore.LIGHTGREEN_EX,
                  Fore.LIGHTBLUE_EX, Fore.LIGHTRED_EX, Fore.GREEN, Fore.BLUE]
        for member in self._get_members(c):
            print('{}{}{}'.format(colors[level], '  '*level, member))
            if level < 5 and not callable(c):
                self._command_tree(getattr(c, member), level + 1)

    def __getattribute__(self, name):
        """Get command (module) info from same named class.

        Loads module_name.ModuleName.run() if exists;
        Loads module_name.ModuleName with public members;
        Loads entire module_name if CamelCased class with module name not exists."""

        # default behavior if name is not module name
        if name == '_modules' or name not in self._modules:
            return super().__getattribute__(name)

        # import module
        module = getattr(__import__(
            '{}.{}'.format(MODULES_DIR, name)), name)

        classname = self._get_classname(name)

        # if class named as {ModuleName} exists
        if hasattr(module, classname):
            module_class = getattr(module, classname)
            if not module_class.__doc__:
                module_class.__doc__ = module.__doc__
            elif not module.__doc__:
                module.__doc__ = module_class.__doc__

            # support for short command, ex: pt ping
            if hasattr(module_class, 'run'):
                return module_class.run

            # then return Class to initialize by `fire` only if needeed
            return module_class

        # if plain module without class, return module
        # as routine with docstring from module (hack for `fire`)
        def plain(): return module
        plain.__doc__ = module.__doc__

        return plain

    @staticmethod
    def _get_classname(module_name):
        """Converts snake_case to CamelCase"""
        return ''.join(x.capitalize() for x in module_name.split('_'))

    @staticmethod
    def _get_members(c):
        return [m for m in c.__dict__.keys() if not m.startswith('_')]
