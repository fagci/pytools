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

    def __getattribute__(self, name):
        """Get command (module) info from same named class"""

        # default behavior if name is not module name
        if name == '_modules' or name not in self._modules:
            return super().__getattribute__(name)

        # import module
        module: ModuleType = getattr(__import__(f'{MODULES_DIR}.{name}'), name)

        classname = self._get_classname(name)

        # if class named as {ModuleName} exists
        if hasattr(module, classname):
            # then return Class to initialize by `fire` only if needeed
            return getattr(module, classname)

        # if plain module without class, return module
        # as routine with docstring from module (hack for `fire`)
        def plain(): return module
        plain.__doc__ = module.__doc__

        return plain

    @staticmethod
    def _get_classname(module_name):
        """Converts snake_case to CamelCase"""
        return ''.join(x.capitalize() for x in module_name.split('_'))
