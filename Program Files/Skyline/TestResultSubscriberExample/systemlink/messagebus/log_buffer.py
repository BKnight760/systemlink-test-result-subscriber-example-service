# -*- coding: utf-8 -*-
"""
Implementation of 'LogBuffer' class
"""
from __future__ import absolute_import

# Import python libs
import datetime

# Import local libs
# pylint: disable=import-error,no-name-in-module
from systemlink.messagebus import trace_logger_messages
# pylint: enable=import-error,no-name-in-module


class LogBuffer(object):
    """
    Log Buffer.

    Buffer to be used for Trace Logger logs.
    """
    def __init__(self):
        self._capacity = 500
        self._entries = []

    def __len__(self):
        """
        Get the current number of entries in the log buffer.

        :return: The current number of entries in the log buffer.
        :rtype: int
        """
        return len(self._entries)

    def __bool__(self):
        """
        Get whether the log buffer is not empty.

        :return: ``True`` if the log buffer is not empty. ``False``
            otherwise.
        :rtype: bool
        """
        return bool(self._entries)

    # Python 2 compatibilty.
    __nonzero__ = __bool__

    def reset(self):
        """
        Remove all entries from the log buffer.
        """
        del self._entries[:]

    def add_entry(self, module_name, trace_point, log_type, log_string):
        """
        Add an entry to the log buffer.

        :param module_name: Name of the module.
        :type module_name: str
        :param trace_point: A TracePoint object representing the
            trace point name to use.
        :type trace_point: systemlink.messagebus.trace_point.TracePoint
        :param log_type: The type of log to use.
        :type log_type: systemlink.messagebus.trace_logger_messages.LogType
        :return: ``True`` if the entry was successfully added. ``False``
            otherwise.
        :rtype: bool
        """
        logged = False
        if trace_point is None:
            trace_point_name = ''
        else:
            trace_point_name = trace_point.name
        if len(self._entries) < self._capacity:
            entry = trace_logger_messages.LogEntry(
                module_name,
                datetime.datetime.utcnow(),
                trace_point_name,
                log_string,
                log_type)
            self._entries.append(entry)
            logged = True
        return logged

    @property
    def entries(self):
        """
        Get the list of entries in this log buffer.

        :return: The list of entries in this log buffer.
        :rtype: list(systemlink.messagebus.trace_logger_messages.LogEntry)
        """
        return self._entries
