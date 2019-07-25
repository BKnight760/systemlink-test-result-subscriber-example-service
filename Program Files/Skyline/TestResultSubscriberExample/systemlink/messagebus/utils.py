# -*- coding: utf-8 -*-
"""
General use utility functions
"""
from __future__ import absolute_import, print_function

# Import python libs
import sys


def is_windows():
    """
    Returns whether the system platform is Windows.

    :return: ``True`` if the system platform is Windows. ``False`` otherwise.
    :rtype: bool
    """
    return sys.platform.startswith('win')


def is_linux():
    """
    Returns whether the system platform is Linux.

    :return: ``True`` if the system platform is Linux. ``False`` otherwise.
    :rtype: bool
    """
    return sys.platform.startswith('linux')


def eprint(*args, **kwargs):
    """
    Print to stderr.

    Takes same parameters as the built-in print command.
    """
    print(*args, file=sys.stderr, **kwargs)


def str_to_bool(src_str, strict=True):
    """
    Convert a :class:`str` to a :class:`bool`.

    :param src_str: The string to convert.
    :type src_str: str
    :param strict: If ``True`` will ensure the false cases
        are checked. If ``False`` will assume if the true case
        is not identified, then the converted value is ``False``.
    :type strict: bool
    :return: The converted boolean value.
    :rtype: bool
    :raises ValueError: if ``strict`` is ``True`` and ``src_str``
        is not identified as a valid true or false value.
    """
    lc_str = src_str.lower()
    if lc_str in ('true', 'yes', 't', '1'):
        return True
    if not strict or lc_str in ('false', 'no', 'f', '0'):
        return False
    raise ValueError('\"{0}\" is not a valid boolean value.'.format(src_str))
