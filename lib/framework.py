"""Toolbox module loader"""
import pkgutil

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
        module = getattr(__import__(f'{MODULES_DIR}.{name}'), name)

        # then return Class to initialize by `fire` only if needeed
        classname = ToolframeLoader._get_classname(name)
        return getattr(module, classname)

    @staticmethod
    def _get_classname(module_name):
        """Converts snake_case to CamelCase"""
        return ''.join(x.capitalize() for x in module_name.split('_'))
