#!/usr/bin/env python
"""Toolbox module loader & executor"""

import pkgutil

import fire

MODULES_DIR = 'tf_modules'


class ToolframeLoader(object):
    """Load modules needed to fire commands"""
    _modules = []

    def __init__(self):
        for module in pkgutil.iter_modules([MODULES_DIR]):
            if not module.name.startswith('_'):
                self._modules.append(module.name)
                setattr(self, module.name, None)


    def __getattribute__(self, name):
        if name == '_modules' or name not in self._modules:
            return super().__getattribute__(name)
        classname = name[0].upper() + name[1:]
        module = getattr(__import__(f'{MODULES_DIR}.{name}'), name)
        return getattr(module, classname)


if __name__ == "__main__":
    fire.Fire(ToolframeLoader)

