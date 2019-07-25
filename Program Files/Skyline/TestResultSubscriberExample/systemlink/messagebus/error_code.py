# -*- coding: utf-8 -*-
"""
Implementation of 'ErrorCode' class
"""
from __future__ import absolute_import


class ErrorCode(object):  # pylint: disable=too-many-public-methods
    """
    Skyline Error Code information.

    For use with the :class:`systemlink.messagebus.error.Error` class.
    """
    def __init__(self, category, name, message=None):
        """
        :param category: The category of the error.
        :type category: str
        :param name: The name of the error.
        :type name: str
        :param message: The error message or ``None`` if there is no error
            message.
        :type message: str or None
        """
        self._category = category
        self._name = name
        self._message = message

    @property
    def category(self):
        """
        Get the category of the error.

        :return: The category of the error.
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category):
        """
        Set the category of the error.

        :param category: The category of the error.
        :type category: str
        """
        self._category = category

    @property
    def name(self):
        """
        Get the name of the error.

        :return: The name of the error.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Set the name of the error.

        :param name: The name of the error.
        :type name: str
        """
        self._name = name

    @property
    def message(self):
        """
        Get the error message.

        :return: The error message or ``None`` if there is no error
            message.
        :rtype: str or None
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Set the error message.

        :param message: The error message or ``None`` if there is no error
            message.
        :type message: str or None
        """
        self._message = message

    def __str__(self):
        """
        Return a string representation of the error code.

        :return: A string representation of the error code.
        :rtype: str
        """
        if not self._category:
            return self._name
        return self._category + '.' + self._name
