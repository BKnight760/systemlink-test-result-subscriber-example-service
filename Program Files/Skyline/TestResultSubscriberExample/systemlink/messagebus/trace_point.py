# -*- coding: utf-8 -*-
"""
Implementation of 'TracePoint' class
"""
from __future__ import absolute_import


class TracePoint(object):
    """
    A Trace Point for use with
    :class:`systemlink.messagebus.trace_logger.TraceLogger`.
    """
    def __init__(self, name, is_enabled=False, full_name=None, declaring_class=None):
        """
        :param name: The name of the Trace Point. ``None`` if no name is used.
        :type name: str or None
        :param is_enabled: ``True`` if the Trace Point is currently enabled.
            ``False`` otherwise.
        :type is_enabled: bool
        :param full_name: The full name of the Trace Point. ``None`` if no
            full name is used.
        :type full_name: str or None
        :param declaring_class: Name of the declaring class. ``None`` if no
            declaring class name is used.
        :type declaring_class: str or None
        """
        self._enabled = bool(is_enabled)
        if name is None:
            self._name = ''
        else:
            self._name = name
        if full_name is None:
            self._full_name = '<unset>'
        else:
            self._full_name = full_name
        if declaring_class is None:
            self._declaring_class = '<unset>'
        else:
            self._declaring_class = declaring_class

    @property
    def name(self):
        """
        Get the name of the Trace Point.

        :return: The name of the Trace Point.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Set the name of the Trace Point.

        :param name: The name of the Trace Point.
        :type name: str
        """
        self._name = name

    @property
    def full_name(self):
        """
        Get the full name of the Trace Point.

        :return: The full name of the Trace Point.
        :rtype: str
        """
        return self._full_name

    @full_name.setter
    def full_name(self, full_name):
        """
        Set the full name of the Trace Point.

        :param full_name: The full name of the Trace Point.
        :type full_name: str
        """
        self._full_name = full_name

    @property
    def declaring_class(self):
        """
        Get the name of the declaring class.

        :return: The name of the declaring class.
        :rtype: str
        """
        return self._declaring_class

    @declaring_class.setter
    def declaring_class(self, declaring_class):
        """
        Set the name of the declaring class.

        :param declaring_class: The name of the declaring class.
        :type declaring_class: str
        """
        self._declaring_class = declaring_class

    @property
    def is_enabled(self):
        """
        Get whether the Trace Point is enabled.

        :return: ``True`` if the Trace Point is enabled. ``False`` otherwise.
        :rtype: bool
        """
        return self._enabled

    def enable(self):
        """
        Enable the Trace Point.
        """
        self._enabled = True

    def disable(self):
        """
        Disable the Trace Point.
        """
        self._enabled = False
