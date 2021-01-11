"""Toolbox module loader"""

MODULES_DIR = 'modules'


class ToolframeLoader(object):
    """Load modules needed to fire up commands"""
    _modules = {}

    def __init__(self):
        """Fill attributes to show as commands"""
        from pkgutil import iter_modules
        for module in iter_modules([MODULES_DIR]):
            if module.name.startswith('_'):
                continue
            self._modules[module.name] = None
            setattr(self, module.name, None)

    def commands(self):
        """List commands as tree"""
        self._command_tree(self)

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

        module = self._modules.get(name)
        if module:
            return self._modules.get(name)

        module = self._get_module(name)
        self._modules[name] = module
        return module

    def _get_module(self, name):
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

            # admin module with modules support
            if name == 'admin':
                return module_class(self._modules).run

            # support for short command, ex: pt ping
            if hasattr(module_class, 'run'):
                return module_class().run

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
