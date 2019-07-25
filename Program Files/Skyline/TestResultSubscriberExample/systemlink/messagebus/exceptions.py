# -*- coding: utf-8 -*-
"""
Implementation of 'SystemLinkException'.
"""
from __future__ import absolute_import

# Import local libs
# pylint: disable=import-error
from systemlink.messagebus import error_code_registry
from systemlink.messagebus.error import Error
# pylint: enable=import-error


class SystemLinkException(Exception):
    """
    Base exception class: all Skyline-specific exceptions should subclass this.
    """
    def __init__(self, error):
        """
        :param error: An instance of :class`systemlink.messagebus.error.Error`.
            May be ``None``.
        :type error: systemlink.messagebus.error.Error or None
        """
        if error is None:
            error_code_obj = error_code_registry.lookup('Skyline.Exception')
            error = Error(error_code=error_code_obj)
        message = error.info
        super(SystemLinkException, self).__init__(message)
        self.message = message
        self.error = error

    @classmethod
    def from_name(cls, qualified_name, info=None, args=None):
        """
        Create a SystemLinkException object based on the qualified name.

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
        :return: An instance of :class:`SystemLinkException`.
        :rtype: SystemLinkException
        """
        error_obj = Error.from_name(qualified_name, info=info, args=args)
        return cls(error=error_obj)

    @classmethod
    def from_error_code(cls, error_code, info=None, args=None):
        """
        Create a SystemLinkException object based on an ErrorCode object.

        :param error_code: An instance of
            :class`systemlink.messagebus.error_code.ErrorCode`. May be
            ``None``.
        :type error_code: systemlink.messagebus.error_code.ErrorCode or None
        :param info: Error information string. May be ``None`` in the cases
            of no error or if this information is desired to be auto-generated
            based on ``error_code`` and ``args``.
        :type info: str or None
        :param args: A list of arguments associated with the error. May be
            ``None`` if the associated error does not have any arguments or
            if ``info`` is not ``None``.
        :type args: list or None
        :return: An instance of :class:`SystemLinkException`.
        :rtype: SystemLinkException
        """
        if error_code is None:
            error_code = error_code_registry.lookup('Skyline.Exception')
        error_obj = Error(error_code=error_code, info=info, args=args)
        return cls(error=error_obj)

    @classmethod
    def from_exception(cls, exc, include_stack=True):
        """
        Create a SystemLinkException object based on an exception.

        :param exc: An instance of a class derived from
            :class:`Exception`.
        :type exc: Exception
        :param include_stack: Whether to include stack information in
            the error message.
        :type include_stack: bool
        :return: An instance of :class:`SystemLinkException`.
        :rtype: SystemLinkException
        """
        if isinstance(exc, cls):
            return exc
        error_obj = Error.from_exception(exc, include_stack=include_stack)
        return cls(error=error_obj)

    def __repr__(self):
        ret = '[{0}] {1}'.format(self.error.name, self.message)
        return ret.strip()

    __str__ = __repr__
