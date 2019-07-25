# -*- coding: utf-8 -*-
"""
Implementation of 'Error' class
"""
from __future__ import absolute_import

# Import python libs
import json
import sys
import traceback

# Import local libs
# pylint: disable=import-error
from systemlink.messagebus import error_code_registry
# pylint: enable=import-error

# Since systemlink.messagebus.exceptions imports this module, we cannot
# import that module at the top level to avoid a circular dependency.


class Error(object):  # pylint: disable=too-many-public-methods
    """
    Skyline Error information.

    Used to encapsulate error information when an error occurs
    in the Skyline framework.
    """
    def __init__(self, error_code=None, info=None, args=None):
        """
        :param error_code: The error code of the error or ``None`` if no
            error has occurred.
        :type error_code: systemlink.messagebus.error_code.ErrorCode or None
        :param info: Error information string. May be ``None`` in the cases
            of no error or if this information is desired to be auto-generated
            based on ``error_code``.
        :type info: str or None
        :param args: A list of arguments associated with the error.
        :type args: list
        """
        self._has_value = False
        self._error_code = None
        self._info = None
        self._args = None
        self.set(error_code, info, args)

    @classmethod
    def from_name(cls, qualified_name, info=None, args=None):
        """
        Create an :class:`Error` instance based on the qualified name.

        :param qualified_name: The qualified name of the error. It is in
            the form ``[category].[name]``. May be ``None``.
        :type qualified_name: str or None
        :param info: Error information string. May be ``None`` in the cases
            of no error or if this information is desired to be auto-generated
            based on ``qualified_name`` and ``args``.
        :type info: str or None
        :param args: A list of arguments associated with the error. May be
            ``None`` if the associated error does not have any arguments or
            if ``info`` is not ``None``.
        :type args: list or None
        :return: An instance of :class:`Error`.
        :rtype: Error
        """
        if qualified_name is None:
            qualified_name = 'Skyline.Exception'
        error_code_obj = error_code_registry.lookup(qualified_name)
        return cls(error_code=error_code_obj, info=info, args=args)

    @classmethod
    def from_exception(cls, exc, include_stack=True):
        """
        Create an :class:`Error` instance based on an exception.

        :param exc: An instance of a class derived from
            :class:`Exception`.
        :type exc: Exception
        :param include_stack: Whether to include stack information in
            the error message.
        :type include_stack: bool
        :return: An instance of :class:`Error`.
        :rtype: Error
        """
        # Import here instead of at the top-level to avoid a circular
        # dependency.
        from systemlink.messagebus.exceptions import SystemLinkException

        if isinstance(exc, SystemLinkException):
            return exc.error

        error_code_obj = error_code_registry.lookup('Skyline.Exception')

        if include_stack:
            exc_tb = sys.exc_info()[2]
            if exc_tb is not None:
                tb_info = traceback.format_tb(exc_tb)
            else:
                tb_info = []
            info = 'Python exception: {0}: {1}\n{2}'.format(
                type(exc).__name__, exc, ''.join(tb_info)).strip()
        else:
            info = 'Python exception: {0}: {1}'.format(type(exc).__name__, exc).strip()

        return cls(error_code=error_code_obj, info=info)

    def set(self, error_code, info, args):
        """
        Set an error.

        :param error_code: The error code of the error or ``None`` if no
            error has occurred.
        :type error_code: systemlink.messagebus.error_code.ErrorCode or None
        :param info: Error information string. May be ``None`` in the cases
            of no error or if this information is desired to be auto-generated
            based on ``error_code``.
        :type info: str or None
        :param args: A list of arguments associated with the error.
        :type args: list
        """
        self._error_code = error_code
        self._info = info
        if self._info is None:
            self._info = ''
        self._args = args
        if self._args is None:
            self._args = []
        self._has_value = bool(error_code is not None)
        if self._has_value and self._error_code._message and info is None:  # pylint: disable=protected-access
            self._info = self._format_message()

    def has_value(self):
        """
        Return whether this :class:`Error` object has a value.

        :return: ``True`` if this :class:`Error` object has a value. ``False``
            otherwise.
        :rtype: bool
        """
        return self._has_value

    def reset(self):
        """
        Reset this :class:`Error` object to a no error state.
        """
        self._has_value = False
        self._error_code = None
        self._info = ''
        self._args = []

    def serialize(self):
        """
        Return a JSON representation of the error string.

        :return: A JSON representation of the error string.
        :rtype: str
        """
        if self._has_value:
            return '\"' + json.loads(str(self)) + '\"'
        return 'null'

    @property
    def name(self):
        """
        Get the error name information.

        :return: The error name information or ``None`` if no error is set.
        :rtype: str or None
        """
        if not self._has_value:
            return None
        return str(self._error_code)

    @property
    def code(self):
        """
        Get the error code.

        :return: The error code or ``None`` if no error is set.
        :rtype: systemlink.messagebus.error_code.ErrorCode or None
        """
        return self._error_code

    @property
    def info(self):
        """
        Get the error information.

        :return: The error information. Will return an
            empty string if there is no associated error information.
        :rtype: str
        """
        return self._info

    @info.setter
    def info(self, info):
        """
        Set the error information.

        :param info: The error information.
        :type info: str
        """
        self._info = info
        if self._info is None:
            self._info = ''

    @property
    def args(self):
        """
        Get the arguments.

        :return: The arguments. Will return an
            empty list if there is no associated arguments.
        :rtype: list
        """
        return self._args

    @args.setter
    def args(self, args):
        """
        Set the arguments.

        :param args: The arguments.
        :type args: list
        """
        self._args = args
        if self._args is None:
            self._args = []

    def __str__(self):
        """
        Return a string representation of the error.

        :return: A string representation of the error.
        :rtype: str
        """
        if not self._has_value:
            return ''
        code = str(self._error_code)
        if not self._info:
            return code
        return code + ': ' + self._info

    def _format_message(self):  # pylint: disable=too-many-branches
        """
        This method performs message inserts on the ErrorCode's message string
        and returns the result. The message format follows the C#
        string.Format(<message>, params ...) syntax.  Message insert arguments
        are denoted by braces enclosing an integer value.  ex:  '{#}' For
        example: "Processing file {0} resulted in {1} failed operation(s)."
        The vector of string arguments included in the Error class is used as
        the positional inserts for the message.

        :return: The formatted message.
        :rtype: str
        """
        if self._args:
            return self._error_code._message.format(*self._args)  # pylint: disable=protected-access
        return self._error_code._message  # pylint: disable=protected-access
