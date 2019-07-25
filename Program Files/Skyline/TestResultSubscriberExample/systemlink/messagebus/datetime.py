# -*- coding: utf-8 -*-
"""
Collection of datetime-related functions.
"""
from __future__ import absolute_import

# Import python libs
import datetime


def from_datetime(datetime_object):
    """
    Converts a :class:`datetime.datetime` object into a string
    which SystemLink interprets as a timestamp. The output
    string is in ISO 8601 format that ends with 'Z'.

    :param datetime_object: A datetime object representing a timestamp.
    :type datetime_object: datetime.datetime
    :return: A string that is in ISO 8601 format that ends with 'Z'.
    :rtype: str
    """
    return datetime_object.isoformat() + 'Z'


def to_datetime(datetime_string):
    """
    Converts a string which SystemLink interprets as a timestamp
    into a :class:`datetime.datetime` object.
    The input string is in ISO 8601 format that ends with 'Z'.
    Will pass through if the input is already an instance of
    :class:`datetime.datetime`.

    :param datetime_string: A string that is in ISO 8601 format that
        ends with 'Z'. Will pass through if this is already an instance
        of :class:`datetime.datetime`.
    :type datetime_string: str or datetime.datetime
    :return: A datetime object representing a timestamp.
    :rtype: datetime.datetime
    """
    if isinstance(datetime_string, datetime.datetime):
        return datetime_string
    if datetime_string.endswith('Z'):
        datetime_string = datetime_string[:-1]
    dot_index = datetime_string.find('.')
    if dot_index != -1:
        # datetime only stores to 6 decimal places (since it stores
        # up to microseconds). Due to this, truncate if necessary.
        if len(datetime_string) - dot_index > 7:
            extra_digits = len(datetime_string) - dot_index - 7
            datetime_string = datetime_string[:-extra_digits]
        format_str = '%Y-%m-%dT%H:%M:%S.%f'
    else:
        format_str = '%Y-%m-%dT%H:%M:%S'
    return datetime.datetime.strptime(datetime_string, format_str)
