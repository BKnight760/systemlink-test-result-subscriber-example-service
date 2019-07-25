# -*- coding: utf-8 -*-
"""
Implementation of 'ProcessLogger' class
"""
from __future__ import absolute_import

# Import python libs
import logging
import sys
import threading
import time

# pylint: disable=import-error
if sys.version_info[0] < 3:
    from Queue import Queue, Full
else:
    from queue import Queue, Full
# pylint: enable=import-error

# Import local libs
# pylint: disable=import-error,wrong-import-position,no-name-in-module
from systemlink.messagebus import trace_logger_messages
from systemlink.messagebus.exceptions import SystemLinkException
from systemlink.messagebus.trace_logger import TraceLogger
from systemlink.messagebus.buffer_pool import BufferPool
from systemlink.messagebus.trace_point import TracePoint
from systemlink.messagebus.log_buffer import LogBuffer
# pylint: enable=import-error,wrong-import-position,no-name-in-module

# Set up logging
LOGGER = logging.getLogger(__name__)

LOG_TYPE_LOG = trace_logger_messages.LogType(trace_logger_messages.LogType.LOG)
LOG_TYPE_INFO = trace_logger_messages.LogType(trace_logger_messages.LogType.INFO)
LOG_TYPE_ERROR = trace_logger_messages.LogType(trace_logger_messages.LogType.ERROR)


class ProcessLogger(object):  # pylint: disable=too-many-public-methods,too-many-instance-attributes
    """
    The Process Logger.

    Used to log messages to the Trace Logger.
    """
    def __init__(self, instance_name, message_service, publish_callback=None,
                 register_broadcast_callback=None):
        """
        :param instance_name: Name of the Process Logger instance.
        :type instance_name: str
        :param message_service: The Message Service to use. If ``None``, then
            ``publish_callback`` must be specified.
        :type message_service: systemlink.messagebus.message_service.MessageService
            or None
        :param publish_callback: The callback for when publishing completes.
            Ignored and may be ``None`` if ``message_service`` is specified.
            This is a callable object or function that takes one argument of type
            :class:`systemlink.messagebus.message_base.MessageBase`.
        :type publish_callback: callable or None
        :param register_broadcast_callback: The callback for when a broadcast
            is registered. Ignored and may be ``None`` if ``message_service``
            is specified. This is a callable object or function that takes
            two arguments, the first argument of type
            :class:`systemlink.messagebus.generic_message.GenericMessage`
            and the second argument is a callable object or function that
            also takes two arguments itself, the first is of type ``type``
            which is the message class type and the second is of type
            :class:`systemlink.messagebus.generic_message.GenericMessage`.
        :type register_broadcast_callback: callable or None
        """
        self._log_to_trace_logger = False
        self._active_log_buffer = LogBuffer()
        if message_service is not None:
            message_service.trace_logger = self.make_trace_logger(message_service.service_name)
        self._stop_logging_thread = False
        self._instance_name = instance_name
        if message_service is not None:
            self._publish_callback = message_service.publisher.publish_message_callback
        else:
            self._publish_callback = publish_callback
        self._buffer_pool = BufferPool()
        self._buffers_ready_to_log = Queue()
        if message_service is not None:
            message_service.register_callback(
                trace_logger_messages.TraceLoggerSnapshotBroadcast,
                self._update_trace_points_callback)
        else:
            register_broadcast_callback(
                trace_logger_messages.TraceLoggerSnapshotBroadcast,
                self._update_trace_points_callback)
        self._trace_points = {}

        self._logging_thread_wakeup_event = threading.Semaphore(0)

        self._logging_thread = threading.Thread(target=self._logging_thread_func)
        self._logging_thread.daemon = True
        self._logging_thread.start()

        # Prompt the TraceLoggerService to broadcast an update
        routed_message = \
            trace_logger_messages.TraceLoggerBroadcastTracePointsRoutedMessage()
        self._publish_callback(routed_message)

    def __del__(self):
        self.close()

    def close(self):
        """
        Close this instance of :class:`ProcessLogger`.
        """
        if self._stop_logging_thread:
            return
        self._stop_logging_thread = True
        self._logging_thread_wakeup_event.release()
        self._logging_thread.join()
        self._logging_thread = None

    def make_trace_logger(self, name, parent=None, log_to_trace_logger=False):
        """
        Create an instance of
        :class:`systemlink.messagebus.trace_logger.TraceLogger`.

        :param name: The last part of the name to use for this Trace Logger.
            Will not be the full name if ``parent`` is not ``None``.
            May be ``None``.
        :type name: str or None
        :param parent: The parent Trace Logger object used to create this one.
            May be ``None``.
        :type parent: systemlink.messagebus.trace_logger.TraceLogger
        :return: A new instance of
            :class:`systemlink.messagebus.trace_logger.TraceLogger`.
        :rtype: systemlink.messagebus.trace_logger.TraceLogger
        :param log_to_trace_logger: ``True`` if the created :class:`TraceLogger`
            instance should automatically send Python logging to the Trace
            Logger service. Only one :class:`TraceLogger` instance may do so
            per :class:`systemlink.messagebus.process_logger.ProcessLogger`
            instance. ``False`` otherwise.
        :type log_to_trace_logger: bool
        """
        return TraceLogger(name, parent, self, log_to_trace_logger=log_to_trace_logger)

    @property
    def current_trace_points(self):
        """
        Get the current trace points.

        :return: The current trace points.
        :rtype: list(systemlink.messagebus.trace_point.TracePoint)
        """
        return list(self._trace_points.values())

    def make_or_lookup_trace_point(self, name):
        """
        Create or find a Trace Point.

        :param name: Name of the Trace Point.
        :type name: str
        :return: The associated Trace Point.
        :rtype: systemlink.messagebus.trace_point.TracePoint
        """
        ret = self._trace_points.get(name)
        if not ret:
            trace_point = TracePoint(name=name)
            self._trace_points[name] = trace_point
            ret = trace_point
        routed_message = \
            trace_logger_messages.TraceLoggerRegisterTracePointRoutedMessage(name)
        routed_message.ignore_response = True
        self._publish_callback(routed_message)
        return ret

    def log(self, logging_module_name, log_string, trace_point=None):
        """
        Log a string to the Trace Logger.

        :param logging_module_name: The name of the module that wants to log.
        :type logging_module_name: str
        :param log_string: The string to log.
        :type log_string: str
        :param trace_point: A
            :class:`systemlink.messagebus.trace_point.TracePoint` object or
            ``None`` if there is no associated Trace Point.
        :type trace_point: systemlink.messagebus.trace_point.TracePoint or None
        """
        self._internal_log(logging_module_name, trace_point, LOG_TYPE_LOG, log_string)

    def log_info(self, logging_module_name, log_string, trace_point=None):
        """
        Log an information string to the Trace Logger.

        :param logging_module_name: The name of the module that wants to log.
        :type logging_module_name: str
        :param log_string: The string to log.
        :type log_string: str
        :param trace_point: A
            :class:`systemlink.messagebus.trace_point.TracePoint` object or
            ``None`` if there is no associated Trace Point.
        :type trace_point: systemlink.messagebus.trace_point.TracePoint or None
        """
        self._internal_log(logging_module_name, trace_point, LOG_TYPE_INFO, log_string)

    def log_error(self, logging_module_name, log_string, trace_point=None):
        """
        Log an error string to the Trace Logger.

        :param logging_module_name: The name of the module that wants to log.
        :type logging_module_name: str
        :param log_string: The string to log.
        :type log_string: str
        :param trace_point: A
            :class:`systemlink.messagebus.trace_point.TracePoint` object or
            ``None`` if there is no associated Trace Point.
        :type trace_point: systemlink.messagebus.trace_point.TracePoint or None
        """
        self._internal_log(logging_module_name, trace_point, LOG_TYPE_ERROR, log_string)

    def _swap_active_buffer(self, mandatory):
        """
        There are 2 buffers in use by the Process Logger. The ``active``
        buffer is of type :class:`systemlink.messagebus.log_buffer.LogBuffer`
        and it is the buffer that is being added to by calls to ``log``,
        ``log_info``, and ``log_error``. The ``ready_to_log`` queue is a
        :class:`queue.Queue` of
        :class:`systemlink.messagebus.log_buffer.LogBuffer` and is used to send
        the log messages via AMQP to the Trace Logger service. This function
        will move the ``active`` buffer to the ``ready_to_log`` queue and
        create a new ``active`` buffer.

        :param mandatory: If ``True``, will always move the ``active``
            buffer to the ``ready_to_log`` queue. If ``False`` will only
            move the ``active`` buffer to the ``ready_to_log`` queue if the
            ``active`` buffer is not empty.
        :type mandatory: bool
        """
        if mandatory or self._active_log_buffer:
            old_buffer = self._active_log_buffer
            self._active_log_buffer = self._buffer_pool.get_buffer()
            try:
                self._buffers_ready_to_log.put_nowait(old_buffer)
            except Full:
                pass

    def _internal_log(self, logging_module_name, trace_point, log_type, log_string):
        """
        Internal function to log to the Trace Logger.

        :param logging_module_name: The name of the module that wants to log.
        :type logging_module_name: str
        :param log_string: The string to log.
        :type log_string: str
        :param trace_point: A
            :class:`systemlink.messagebus.trace_point.TracePoint` object or
            ``None`` if there is no associated Trace Point.
        :type trace_point: systemlink.messagebus.trace_point.TracePoint or None
        """
        if not self._stop_logging_thread:
            logged = self._active_log_buffer.add_entry(
                logging_module_name, trace_point, log_type, log_string
            )
            if logged:
                return
            self._swap_active_buffer(True)
            self._logging_thread_wakeup_event.release()
            self._active_log_buffer.add_entry(
                logging_module_name, trace_point, log_type, log_string
            )

    def _logging_thread_func(self):
        """
        The thread function for logging.

        It will write the log immediately if the logging thread wakeup event
        is set. Otherwise, it will wait 100 milliseconds and then log.
        On exit, it will also log everything left in the buffer.
        """
        try:
            while not self._stop_logging_thread:
                if sys.version_info[0] >= 3:
                    self._logging_thread_wakeup_event.acquire(timeout=0.1)  # pylint: disable=unexpected-keyword-arg
                elif not self._logging_thread_wakeup_event.acquire(blocking=False):
                    time.sleep(0.1)
                if self._buffers_ready_to_log.empty():
                    self._swap_active_buffer(False)
                self._write_the_log()
        except (KeyboardInterrupt, SystemExit):
            LOGGER.debug('ProcessLogger logging_thread exiting due to process exit')
        self._swap_active_buffer(True)
        self._write_the_log()

    def _write_the_log(self):
        """
        Write everything currently in the ``self._buffers_ready_to_log`` queue
        to the Trace Logger service. It will stop logging if it encounters a
        :class:`systemlink.messagebus.exceptions.SystemLinkException`.
        """
        done = False
        while not done:
            if not self._buffers_ready_to_log.empty():
                ready_buffer = self._buffers_ready_to_log.get_nowait()

                routed_message = (
                    trace_logger_messages.TraceLoggerStoreEntriesRoutedMessage(
                        ready_buffer.entries
                    )
                )
                routed_message.ignore_response = True

                try:
                    self._publish_callback(routed_message)
                    self._buffer_pool.return_buffer(ready_buffer)
                except SystemLinkException:
                    done = True
            else:
                done = True

    @property
    def log_to_trace_logger(self):
        """
        Get whether this ProcessLogger instance is automatically sending
        Python logging to the Trace Logger service.

        :return: ``True`` if Python logging is automatically sent to
            the Trace Logger service. ``False`` otherwise.
        :rtype: bool
        """
        return self._log_to_trace_logger

    def _update_trace_points_callback(self, generic_message):
        """
        This is invoked by the framework as a callback when a message is
        received that triggers the condition of the callback.

        :param generic_message: The message received that triggered this callback.
        :type generic_message: :class:`systemlink.messagebus.generic_message.GenericMessage`
        """
        snapshot = trace_logger_messages.TraceLoggerSnapshotBroadcast.from_message(generic_message)
        if not snapshot.settings:
            return

        lc_instance_name = self._instance_name.lower()

        for trace_point_setting in snapshot.settings:
            name = trace_point_setting.name
            trace_point_value = trace_point_setting.enabled

            for trace_point_exception in trace_point_setting.exceptions:
                if trace_point_exception.lower() == lc_instance_name:
                    trace_point_value = not trace_point_setting.enabled
                    break

            trace_point = self._trace_points.get(name)
            if trace_point is None:
                trace_point = TracePoint(name)
                if trace_point_value:
                    trace_point.enable()
                else:
                    trace_point.disable()

                self._trace_points[name] = trace_point
            else:
                if trace_point.is_enabled != trace_point_value:
                    if trace_point_value:
                        trace_point.enable()
                    else:
                        trace_point.disable()
