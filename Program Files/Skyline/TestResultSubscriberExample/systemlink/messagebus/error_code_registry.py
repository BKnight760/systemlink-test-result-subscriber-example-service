# -*- coding: utf-8 -*-
"""
Functions that assist in registering and using error names, codes, and
messages.
"""
from __future__ import absolute_import

# Import local libs
# pylint: disable=import-error
import systemlink.messagebus.error_code as error_code_mod
# pylint: enable=import-error

# Since systemlink.messagebus.exceptions imports this module, we cannot
# import that module at the top level to avoid a circular dependency.

ERROR_NAME_TO_CODE_MAP = {
    '': error_code_mod.ErrorCode('', 'Unknown', 'An unknown error occurred.')
}
ERROR_NAME_TO_NUMERIC_CODE_MAP = {}
NUMERIC_CODE_TO_ERROR_NAME_MAP = {}


def is_registered():
    """
    Check if the Error Code Registry has any registered entries.

    :return: ``True`` if any entries were registered. ``False`` otherwise.
    :rtype: bool
    """
    return len(ERROR_NAME_TO_CODE_MAP) > 1


def register(category, name, message, numeric_error_code=None):
    """
    Register an error code.

    :param category: The category of the error.
    :type category: str
    :param name: The name of the error.
    :type name: str
    :param message: The error message.
    :type message: str
    :param numeric_error_code: The associated numeric error code.
    :type numeric_error_code: int or None
    :return: The created
        :class:`systemlink.messagebus.error_code.ErrorCode` instance.
    :rtype: systemlink.messagebus.error_code.ErrorCode
    """
    error_code_obj = error_code_mod.ErrorCode(category, name, message)
    qualified_name = str(error_code_obj)
    ERROR_NAME_TO_CODE_MAP[qualified_name] = error_code_obj
    if numeric_error_code is not None:
        ERROR_NAME_TO_NUMERIC_CODE_MAP[qualified_name] = numeric_error_code
        NUMERIC_CODE_TO_ERROR_NAME_MAP[numeric_error_code] = qualified_name
    return error_code_obj


def _unknown_error_code(qualified_name):
    """
    Return an error code based on an unknown
    qualified name.

    :param qualified_name: The qualified name of the error. It is in
        the form ``[category].[name]``.
    :type qualified_name: str
    :return: A
        :class:`systemlink.messagebus.error_code.ErrorCode` instance.
    :rtype: systemlink.messagebus.error_code.ErrorCode
    """
    sep_idx = qualified_name.find('.')
    if sep_idx == -1:
        category = ''
        name = ''
    else:
        category = qualified_name[0:sep_idx]
        name = qualified_name[sep_idx+1:]
    error_code_obj = error_code_mod.ErrorCode(category, name)
    return error_code_obj


def lookup(qualified_name):
    """
    Look up an error code.

    :param qualified_name: The qualified name of the error. It is in
        the form ``[category].[name]``.
    :type qualified_name: str
    :return: A
        :class:`systemlink.messagebus.error_code.ErrorCode` instance.
    :rtype: systemlink.messagebus.error_code.ErrorCode
    """
    error_code_obj = ERROR_NAME_TO_CODE_MAP.get(qualified_name)
    if error_code_obj is not None:
        return error_code_obj
    return _unknown_error_code(qualified_name)


def format_message(uninserted_message, args=None):
    """
    Format an error message.

    :param uninserted_message: The unformatted error message.
    :type uninserted_message: str
    :param args: A list of arguments (if needed) for the error message.
    :type args: list or None
    :return: The formatted error message.
    :rtype: str
    """
    if args:
        return uninserted_message.format(*args)
    return uninserted_message


def get_error_message_by_name(qualified_name, args=None):
    """
    Get an error message based on the error qualified name.

    :param qualified_name: The qualified name of the error. It is in
        the form ``[category].[name]``.
    :type qualified_name: str
    :param args: A list of arguments (if needed) for the error message.
    :type args: list or None
    :return: The formatted error message.
    :rtype: str
    """
    error_code_obj = lookup(qualified_name)
    msg = error_code_obj.message
    return format_message(msg, args)


def get_error_message_by_numeric_code(numeric_error_code, args=None):  # pylint: disable=invalid-name
    """
    Get an error message based on the error name.

    :param numeric_error_code: The numeric error code.
    :type numeric_error_code: int
    :param args: A list of arguments (if needed) for the error message.
    :type args: list or None
    :return: The formatted error message.
    :rtype: str
    """
    error_name = get_error_name_by_numeric_code(numeric_error_code)
    return format_message(lookup(error_name).message, args)


def get_numeric_error_code(qualified_name):
    """
    Get the numeric error code based on the qualified name.

    :param qualified_name: The qualified name of the error. It is in
        the form ``[category].[name]``.
    :type qualified_name: str
    :return: The numeric error code.
    :rtype: int
    """
    return ERROR_NAME_TO_NUMERIC_CODE_MAP.get(qualified_name, -251000)


def get_error_name_by_numeric_code(numeric_error_code):
    """
    Get the qualified name of the error based on the numeric error
    code.

    :param numeric_error_code: The numeric error code.
    :type numeric_error_code: int
    :return: The qualified name of the error. It is in
        the form ``[category].[name]``.
    :rtype: str
    """
    return NUMERIC_CODE_TO_ERROR_NAME_MAP.get(numeric_error_code, '')
