#!/usr/bin/env python
"""Toolbox module loader & executor"""

import pkgutil

import fire


class ToolframeLoader(object):
    _modules = []

    def __init__(self):
        for m in pkgutil.iter_modules(['tf_modules']):
            if m.name != 'module':
                self._modules.append(m.name)
                setattr(self, m.name, None)


    def __getattribute__(self, name):
        if name == '_modules' or name not in self._modules:
            return super().__getattribute__(name)
        module_name = f'tf_modules.{name}'
        classname = name[0].upper() + name[1:]
        print(f'Importing {module_name}')
        m = __import__(module_name)
        return getattr(getattr(m, name), classname)()


if __name__ == "__main__":
    mods = {}
    fire.Fire(ToolframeLoader)

