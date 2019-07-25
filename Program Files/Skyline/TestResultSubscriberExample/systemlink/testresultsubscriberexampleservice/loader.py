# -*- coding: utf-8 -*-
"""
Dynamic loader functionality.
"""
from __future__ import absolute_import, print_function

# Import python libs
import importlib.machinery  # pylint: disable=no-name-in-module,import-error
import importlib.util  # pylint: disable=no-name-in-module,import-error
import os.path
import sys


def _add_category_to_paths(category, paths):
    """
    Helper function to add category to search paths.

    :param category: The category name of the plugin. This corresponds
        to the subdirectory that the plugin module is under.
    :type category: str
    :param paths: The search paths to add the category to.
    :type paths: list(str) or None
    :return: The modified search paths
    :rtype: list(str)
    """
    ret = []
    if not paths:
        return ret

    for path in paths:
        if os.path.basename(path) == category:
            ret.append(path)
        else:
            ret.append(os.path.join(path, category))
    return ret


def get_available_plugins(category, additional_search_paths=None):
    """
    Get a list of available plugins by category.

    :param category: The category name of the plugin. This corresponds
        to the subdirectory that the plugin module is under.
    :type category: str
    :param additional_search_paths: Addition paths to search in. These
        will take priority over the default path.
    :type additional_search_paths: list(str) or None
    :return: A list of available plugins.
    :rtype: list(str)
    """
    ret = []

    search_paths = _add_category_to_paths(category, additional_search_paths)
    search_paths.append(
        os.path.join(
            os.path.dirname(__file__),
            category
        )
    )

    for path in search_paths:
        if not os.path.isdir(path):
            continue
        for name in os.listdir(path):
            # Modules starting with underscore are considered private
            # modules and will not be returned in this list.
            if name.endswith('.py') and not name.startswith('_'):
                ret.append(name[:-3])
    return ret


def load_plugin(category, name, additional_search_paths=None, force_reload=False):
    """
    Dynamically load a plugin module.

    :param category: The category name of the plugin. This corresponds
        to the subdirectory that the plugin module is under.
    :type category: str
    :param name: The name of the plugin module to load. The ``.py``
        extension should be omitted from the name.
    :type name: str
    :param additional_search_paths: Addition paths to search in. These
        will take priority over the default path.
    :type additional_search_paths: list(str) or None
    :param force_reload: ``True`` if the module should be reloaded
        even if it was previously loaded. ``False`` otherwise.
    :type force_reload: bool
    :return: The loaded module.
    :rtype: types.ModuleType
    """
    mod_namespace = 'systemlink.testnotifierservice.{0}.{1}'.format(
        category, name
    )
    if not force_reload and mod_namespace in sys.modules:
        return sys.modules[mod_namespace]

    search_paths = _add_category_to_paths(category, additional_search_paths)
    search_paths.append(
        os.path.join(
            os.path.dirname(__file__),
            category
        )
    )

    fname = name + '.py'
    fpath = None
    for path in search_paths:
        test_fpath = os.path.join(path, fname)
        if os.path.isfile(test_fpath):
            fpath = test_fpath
            break
    if not fpath:
        raise ModuleNotFoundError(  # pylint: disable=undefined-variable
            'Could not find plug-in module "{0}" in category "{1}"'
            ''.format(name, category)
        )

    loader = importlib.machinery.SourceFileLoader(mod_namespace, fpath)  # pylint: disable=no-member
    spec = importlib.util.spec_from_loader(loader.name, loader)  # pylint: disable=no-member
    mod = importlib.util.module_from_spec(spec)  # pylint: disable=no-member
    spec.loader.exec_module(mod)
    sys.modules[mod_namespace] = mod
    return mod
