"""Toolbox module loader"""
import pkgutil
from types import ModuleType

MODULES_DIR = 'modules'


class ToolframeLoader(object):
    """Load modules needed to fire up commands"""
    _modules = []

    def __init__(self):
        """Fill attributes to show as commands"""
        for module in pkgutil.iter_modules([MODULES_DIR]):
            if not module.name.startswith('_'):
                self._modules.append(module.name)
                setattr(self, module.name, None)

    @staticmethod
    def _get_members(c):
        members = {}
        for member in c.__dict__.keys():
            if not member.startswith('_'):
                members[member] = getattr(c, member)
        return members

    def commands(self):
        """List commands as tree"""
        for member, c in self._get_members(self).items():
            print('{}'.format(member))
            for subm, sc in self._get_members(c).items():
                print('  {}'.format(subm))

    def __getattribute__(self, name):
        """Get command (module) info from same named class.

        Loads module_name.ModuleName.run() if exists;
        Loads module_name.ModuleName with public members;
        Loads entire module_name if CamelCased class with module name not exists."""

        # default behavior if name is not module name
        if name == '_modules' or name not in self._modules:
            return super().__getattribute__(name)

        # import module
        module: ModuleType = getattr(__import__(
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
