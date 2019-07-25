# -*- coding: utf-8 -*-
"""
Implementation of 'MessageSubscriber' and related classes
"""
from __future__ import absolute_import

# Import python libs
import datetime
import logging
import threading
import sys
import time
# pylint: disable=import-error
if sys.version_info[0] < 3:
    from Queue import Queue, Empty
else:
    from queue import Queue, Empty
# pylint: enable=import-error

# Import local libs
# pylint: disable=wrong-import-position,import-error
from systemlink.messagebus.message_subscriber_builder import MessageSubscriberBuilder
from systemlink.messagebus.amqp_connection_manager import AmqpConnectionManager
from systemlink.messagebus.amqp_consumer_builder import AmqpConsumerBuilder
from systemlink.messagebus.amqp_consumer import AmqpConsumer
from systemlink.messagebus.broadcast_message import BroadcastMessage
from systemlink.messagebus.trace_point import TracePoint
# pylint: enable=wrong-import-position,import-error

# Set up logging
LOGGER = logging.getLogger(__name__)

if sys.version_info[0] < 3:
    # Python 2 does not have built-in support for the monotonic clock.
    # We will use the system clock in this case, which is unsafe since the
    # clock can be changed mid-operation. Eventually, we will drop Python 2
    # support and this logic can disappear.
    USE_MONOTONIC_CLOCK = False
else:
    USE_MONOTONIC_CLOCK = True


class MessageSubscriber(object):  # pylint: disable=too-many-instance-attributes
    """
    The Message Publisher.

    This class is used to subscribe to and consume messages.
    """
    def __init__(self, builder=None):
        """
        :param builder: A
            :class:`systemlink.messagebus.message_subsciber_builder.MessageSubscriberBuilder`
            object used in the construction of this object. May be ``None`` if default
            behavior is desired.
        :type builder:
            systemlink.messagebus.message_subsciber_builder.MessageSubscriberBuilder
        """
        self._closing = False
        self._amqp_connection_manager = builder.connection_manager
        self._amqp_consumers = []
        self._msg_name_callbacks = {}
        self._corr_id_callbacks = {}
        self._sync_callbacks = {}
        self._queue_name = builder.queue_name
        self._explicit_ack = builder.explicit_ack
        self._correlation_id_timeout = builder.correlation_id_timeout
        self._local_message_queue = None
        self._owns_default_binding = False

        if USE_MONOTONIC_CLOCK:
            clock_info = time.get_clock_info('monotonic')  # pylint: disable=no-member
            if clock_info.adjustable:
                self._clock_res = clock_info.resolution
            else:
                self._clock_res = 1
            self._last_correlation_id_check = time.monotonic()  # pylint: disable=no-member
        else:
            self._clock_res = None
            self._last_correlation_id_check = datetime.datetime.utcnow()

        self._callback = builder.callback
        self._trace_unhandled_message = TracePoint('UnhandledMessage')
        self._trace_logger = builder.trace_logger
        if self._trace_logger is not None:
            self._trace_unhandled_message = self._trace_logger.make_trace_point('UnhandledMessage')
        self._message_handling_threads = []
        if builder.local_queue_task_threads > 1:
            self._local_message_queue = Queue(builder.max_local_queue_depth)
            for _ in range(builder.local_queue_task_threads):
                thread = threading.Thread(target=self._process_message_from_local_queue)
                thread.daemon = True
                thread.start()
                self._message_handling_threads.append(thread)
        for _ in range(builder.number_of_amqp_consumers):
            self._amqp_consumers.append(self._create_consumer(builder))
        if builder.register_default_binding:
            params = [self._queue_name, '#']
            self.register_binding(params)
            if builder.is_instance_subscriber:
                self._owns_default_binding = True
        if builder.auto_start_consumers:
            self.start_handling_messages()

    @classmethod
    def from_queue_name(cls, queue_name):
        """
        Create an instance of :class:`MessageSubscriber` based on the
        message queue name.

        :param queue_name: The message queue name.
        :type queue_name: str
        :return: An instance of :class:`MessageSubscriber`.
        :rtype: MessageSubscriber
        """
        builder = MessageSubscriberBuilder(queue_name)
        return cls(builder)

    def __del__(self):
        self.close()

    def close(self):
        """
        Close this instance of :class:`MessageSubscriber`.
        """
        if self._closing:
            return
        self._closing = True

        self.stop_handling_messages()
        if self._owns_default_binding:
            params = [self._queue_name, '#']
            try:
                self.unregister_binding(params)
            except Exception:  # pylint: disable=broad-except
                pass
        if self._message_handling_threads:
            for _ in range(len(self._message_handling_threads)):
                self._local_message_queue.put(None)
            for thread in self._message_handling_threads:
                thread.join()
        if self._amqp_consumers is not None:
            for amqp_consumer in self._amqp_consumers:
                amqp_consumer.close()
            self._amqp_consumers = None

    @property
    def callback(self):
        """
        Get the callback object that is invoked whenever a message is
        received by this subscriber unless there is a more specific
        callback registered.

        :return: The callback for handling messages. This
            is a callable object or function that takes one argument of type
            :class:`systemlink.messagebus.generic_message.GenericMessage`.
        :rtype: callable
        """
        return self._callback

    @callback.setter
    def callback(self, callback):
        """
        Set the callback object that is invoked whenever a message is
        received by this subscriber unless there is a more specific
        callback registered.

        :param callback: The callback for handling messages. This
            is a callable object or function that takes one argument of type
            :class:`systemlink.messagebus.generic_message.GenericMessage`.
        :type callback: callable
        """
        self._callback = callback

    @property
    def trace_logger(self):
        """
        Get the Trace Logger.

        :return: The Trace Logger. May be ``None``
        :rtype: systemlink.messagebus.trace_logger.TraceLogger
            or None
        """
        return self._trace_logger

    @trace_logger.setter
    def trace_logger(self, trace_logger):
        """
        Set the Trace Logger.

        :param trace_logger: The Trace Logger. May be ``None``
        :type trace_logger: systemlink.messagebus.trace_logger.TraceLogger
            or None
        """
        self._trace_logger = trace_logger

    def start_handling_messages(self):
        """
        Start handling incoming messages to all associated
        consumers.
        """
        for amqp_consumer in self._amqp_consumers:
            amqp_consumer.start_handling_messages()

    def stop_handling_messages(self):
        """
        Stop handling incoming messages to all associated
        consumers.
        """
        for amqp_consumer in self._amqp_consumers:
            amqp_consumer.stop_handling_messages()

    def acknowledge_message(self, consumer_tag, delivery_tag):
        """
        Acknowledge a message (meaning that it has been processed by a
        consumer that is part of this Message Subscriber).

        :param consumer_tag: The consumer tag. This is a unique identifier
            for a consumer.
        :type consumer_tag: str
        :param delivery_tag: The message delivery tag.
        :type delivery_tag: str
        """
        for consumer in self._amqp_consumers:
            if consumer.consumer_tag == consumer_tag:
                consumer.acknowledge_message(delivery_tag)
                break

    def not_acknowledge_message(self, consumer_tag, delivery_tag):
        """
        Not acknowledge a message (meaning that it will not be processed by
        tha consumer that is part of this Message Subscriber).

        :param consumer_tag: The consumer tag. This is a unique identifier
            for a consumer.
        :type consumer_tag: str
        :param delivery_tag: The message delivery tag.
        :type delivery_tag: str
        """
        for consumer in self._amqp_consumers:
            if consumer.consumer_tag == consumer_tag:
                consumer.not_acknowledge_message(delivery_tag)
                break

    @staticmethod
    def wait_for_message(queue_, block, timeout_seconds):
        """
        Wait for a message to appear on the queue.

        :param queue_: The queue to wait for the message on.
        :type queue_: queue.Queue
        :param block: ``True`` if we block to wait for the next
            message. ``False`` if we return immediately.
        :type block: bool
        :param timeout_seconds: The number of seconds to wait if ``block`` is
            ``True``. Use ``None`` to wait indefinitely. Ignored if ``block``
            is ``False``.
        :type timeout_seconds: int or float or None
        :return: The message or ``None`` if no message was found
            during the waiting period.
        :rtype: systemlink.messagebus.generic_message.GenericMessage or None
        """
        try:
            return queue_.get(block, timeout_seconds)
        except Empty:
            return None

    def register_callback(self, message_class_type, callback, message_name=None,
                          explicit_ack=False):
        """
        Register a callback that will be invoked when a
        specified message class type is used.

        :param message_class_type: The type of the message class to as the
            trigger for the callback.
        :type message_class_type: type
        :param callback: The callback to invoke. This
            is a callable object or function that takes one argument of type
            :class:`systemlink.messagebus.generic_message.GenericMessage`.
        :type callback: callable
        :param message_name: The message name to use. If ``None``, will
            use the name associated with ``message_class_type``.
        :type message_name: str or None
        :param explicit_ack: If ``True``, it means that the ``callback`` is
            responsible for acknowledging the message. If ``False``, it means
            that this Message Subscriber is responsible for acknowledging the
            message (if the
            :class:`systemlink.messagebus.message_subsciber_builder.MessageSubscriberBuilder`
            object used to create this object has enabled explicit
            acknowledgements).
        :type explicit_ack: bool
        """
        if message_name is None:
            if hasattr(message_class_type, 'MESSAGE_NAME'):
                message_name = message_class_type.MESSAGE_NAME
            else:
                message_name = message_class_type.__name__
        if issubclass(message_class_type, BroadcastMessage):
            binding_params = [message_name]
            self.register_binding(binding_params)
        self.register_message_name_callback(message_name, callback, explicit_ack)

    def unregister_callback(self, message_class_type, message_name=None):
        """
        Unregister a callback that would have been invoked when a
        specified message class type is used.

        :param message_class_type: The name of the message to use as the
            trigger for the callback.
        :type message_class_type: type
        :param message_name: The message name to use. If ``None``, will
            use the name associated with ``message_class_type``.
        :type message_name: str or None
        """
        if message_name is None:
            if hasattr(message_class_type, 'MESSAGE_NAME'):
                message_name = message_class_type.MESSAGE_NAME
            else:
                message_name = message_class_type.__name__
        if issubclass(message_class_type, BroadcastMessage):
            binding_params = [message_name]
            self.unregister_binding(binding_params)
        self.unregister_message_name_callback(message_name)

    def register_message_name_callback(self, message_name, callback, explicit_ack=False):
        """
        Register a callback that will be invoked when a
        certain message name is used in an incoming message.

        :param message_name: The name of the message to use as the
            trigger for the callback.
        :type message_name: str
        :param callback: The callback to invoke. This
            is a callable object or function that takes one argument of type
            :class:`systemlink.messagebus.generic_message.GenericMessage`.
        :type callback: callable
        :param explicit_ack: If ``True``, it means that the ``callback`` is
            responsible for acknowledging the message. If ``False``, it means
            that this Message Subscriber is responsible for acknowledging the
            message (if the
            :class:`systemlink.messagebus.message_subsciber_builder.MessageSubscriberBuilder`
            object used to create this object has enabled explicit
            acknowledgements).
        :type explicit_ack: bool
        """
        info = MessageNameCallbackInfo(callback, explicit_ack)
        self._msg_name_callbacks[message_name] = info

    def unregister_message_name_callback(self, message_name):  # pylint: disable=invalid-name
        """
        Unregister a callback that would have been invoked when a
        certain message name is used in an incoming message.

        :param message_name: The name of the message to use as the
            trigger for the callback.
        :type message_name: str
        """
        if message_name not in self._msg_name_callbacks:
            msg = (
                'Failed to remove message name callback | ' +
                self._queue_name +
                ' | ' +
                message_name
            )
            LOGGER.error(msg)
            if self._trace_logger is not None:
                self._trace_logger.log_error(msg, skip_if_has_log_handler=True)
        else:
            del self._msg_name_callbacks[message_name]

    def register_correlation_id_callback(self, correlation_id, callback, state):  # pylint: disable=invalid-name
        """
        Register a callback that will be invoked when a
        certain correlation ID is used in an incoming message.

        :param correlation_id: The correlation ID to use as the
            trigger for the callback.
        :type correlation_id: str
        :param callback: A class instance that contains a method
            named ``callback``. The ``callback`` function takes an argument of
            type :class:`systemlink.messagebus.generic_message.GenericMessage`
            and a second argument that could be any type for user specific
            data.
        :type callback: object
        :param state: Optional user specific data. May be any
            type.
        :type state: object or None
        """
        if correlation_id is None:
            return
        info = CorrIdCallbackInfo(callback, state)
        self._corr_id_callbacks[correlation_id] = info

    def register_binding(self, binding_parameters):
        """
        Register a binding for all consumers.

        :param binding_parameters: A list of strings that represent a routing key.
        :type binding_parameters: list(str)
        """

        for consumer in self._amqp_consumers:
            consumer.register_binding(binding_parameters)

    def unregister_binding(self, binding_parameters):
        """
        Unregister a binding for all consumers.

        :param binding_parameters: A list of strings that represent a routing key.
        :type binding_parameters: list(str)
        """
        for consumer in self._amqp_consumers:
            consumer.unregister_binding(binding_parameters)

    def _process_message_from_local_queue(self):  # pylint: disable=invalid-name
        """
        Thread function for the local queue task threads.

        Will get a message from the local queue and process it.
        """
        try:
            while True:
                message = self._local_message_queue.get()
                if message is None:
                    break
                self._process_message(message)
                self._local_message_queue.task_done()
        except (KeyboardInterrupt, SystemExit):
            LOGGER.debug('MessageSubscriber _process_message_from_local_queue '
                         'exiting due to process exit')

    def _process_message(self, message):  # pylint: disable=too-many-branches
        """
        Used to allow invoking user defined callbacks for incoming messages
        at various levels.

        Only one is invoked per message, in the following priority:
            1) Callbacks with ``state`` specific to the corrlation ID.
            2) Callbacks without ``state`` specific to the message name.
            3) General callbacks without ``state`` (user defined data).

        :param message: The incoming message to process.
        :type message: systemlink.messagebus.generic_message.GenericMessage
        """
        msg_name_callback_info = None
        corr_id_info = None
        if message.correlation_id in self._corr_id_callbacks:
            corr_id_info = self._corr_id_callbacks[message.correlation_id]
            del self._corr_id_callbacks[message.correlation_id]
        if message.message_name in self._msg_name_callbacks:
            msg_name_callback_info = self._msg_name_callbacks[message.message_name]
        if corr_id_info is not None:
            corr_id_info.callback(message, corr_id_info._state)  # pylint: disable=protected-access
        elif msg_name_callback_info is not None:
            if self._explicit_ack and not msg_name_callback_info.explicit_ack:
                self.acknowledge_message(message.consumer_tag, message.deliver_tag)
            if msg_name_callback_info.callback is not None:
                msg_name_callback_info.callback(message)
        elif self._callback is not None:
            self._callback(message)
        elif message.has_error():
            msg = (
                'Unhandled message ' +
                message.message_name +
                ' Origin=' + message.origin +
                ' Error=' + str(message.error)
            )
            LOGGER.error(msg)
            if self._trace_logger is not None:
                self._trace_logger.log_error(msg, skip_if_has_log_handler=True)
        elif self._trace_logger is not None and self._trace_unhandled_message.is_enabled:
            self._trace_logger.log(self._trace_unhandled_message, message.message_name)
        else:
            # pylint: disable=fixme
            # TODO add support for creating a unhandled message callback.
            # pylint: enable=fixme
            msg = 'Unhandled message: ' + message.message_name
            if self._amqp_connection_manager is not None:
                self._amqp_connection_manager.put_status_message(
                    msg, False, replace_if_full=True
                )
            else:
                AmqpConnectionManager.get_instance().put_status_message(
                    msg, False, replace_if_full=True
                )
        self._purge_correlation_id_callbacks()

    def _purge_correlation_id_callbacks(self):  # pylint: disable=no-self-use
        """
        Traverse all stored correlation ID callbacks and remove them if
        they are older than the correlation ID timeout.
        """
        if USE_MONOTONIC_CLOCK:
            now = time.monotonic()  # pylint: disable=no-member
            diff_seconds = (
                (now - self._correlation_id_timeout) /
                self._clock_res
            )
            if diff_seconds < self._correlation_id_timeout:
                return
            self._correlation_id_timeout = now
            remove_list = []
            for corr_id, callback_info in self._corr_id_callbacks.items():
                diff_seconds = (
                    (now - callback_info.timestamp) /
                    self._clock_res
                )
                if diff_seconds < self._correlation_id_timeout:
                    continue
                remove_list.append(corr_id)
        else:
            now = datetime.datetime.utcnow()
            diff_obj = now - self._correlation_id_timeout
            diff_seconds = diff_obj.microseconds() / 1000000.0
            if diff_seconds < self._correlation_id_timeout:
                return
            self._correlation_id_timeout = now
            remove_list = []
            for corr_id, callback_info in self._corr_id_callbacks.items():
                diff_obj = now - callback_info.timestamp
                diff_seconds = diff_obj.microseconds() / 1000000.0
                if diff_seconds < self._correlation_id_timeout:
                    continue
                remove_list.append(corr_id)

        for corr_id in remove_list:
            del self._corr_id_callbacks[corr_id]
            if (self._trace_logger and self._trace_unhandled_message and
                    self._trace_unhandled_message.is_enabled):
                self._trace_logger.log(
                    'Purged CorrelationIdCallback for ' + corr_id,
                    self._trace_unhandled_message
                )

    def _create_consumer(self, builder):
        """
        Create an instance of
        :class:`systemlink.messagebus.amqp_consumer.AmqpConsumer`.

        :param builder: A
            :class:`systemlink.messagebus.message_subscriber_builder.MessageSubscriberBuilder`
            object.
        :type builder: systemlink.messagebus.message_subscriber_builder.MessageSubscriberBuilder
        :return: A new instance of
            :class:`systemlink.messagebus.amqp_consumer.AmqpConsumer`.
        :rtype: systemlink.messagebus.amqp_consumer.AmqpConsumer
        """
        LOGGER.debug('MessageSubscriber CreateConsumer!')
        consumer_builder = AmqpConsumerBuilder(builder.queue_name, self._handle_message)
        consumer_builder.message_returned_callback = self._handle_message_returned
        consumer_builder.connection_manager = builder.connection_manager
        consumer_builder.durable_queue = builder.durable_queue
        consumer_builder.explicit_ack = builder.explicit_ack
        consumer_builder.prefetch_queue_depth = builder.prefetch_queue_depth
        consumer_builder.trace_logger = builder.trace_logger
        return AmqpConsumer(consumer_builder)

    def _handle_message(self, generic_message):
        """
        Handle a message by either queuing it to let the local message
        queue task threads process it, or process it directly if such
        threads are not set up.

        :param generic_message: The incoming message to handle. The
            class of the message is
            :class:`systemlink.messagebus.generic_message.GenericMessage`.
        :type generic_message: systemlink.messagebus.generic_message.GenericMessage
        """
        info = self._sync_callbacks.get(  # pylint: disable=protected-access
            generic_message.correlation_id
        )
        if info is not None:
            info._queue.put(generic_message)  # pylint: disable=protected-access
        elif self._local_message_queue is not None:  # pylint: disable=protected-access
            self._local_message_queue.put(generic_message)  # pylint: disable=protected-access
        else:
            self._process_message(generic_message)  # pylint: disable=protected-access

    def _handle_message_returned(self, correlation_id, message_type):
        """
        Handle the case when a mandatory delivery could not be honored.

        We must cancel the synchronous wait (to avoid waiting for the
        rest of the timeout) and remove the synchronous and
        correlation ID callbacks.

        :param correlation_id: The correlation ID of the returned message.
        :type correlation_id: str
        :param message_type: The message type of the returned message.
        :type message_type: str
        """
        info = self._sync_callbacks.pop(  # pylint: disable=protected-access
            correlation_id, None
        )
        if info is not None:
            queue_ = info.queue
            while not queue_.empty():
                queue_.get_nowait()

            msg = (
                'Publish failed: The message with mandatory routing could not be delivered. '
                'Message type: {0}, correlation id: {1}'.format(message_type, correlation_id)
            )

            # Cancel the synchronous callback that is waiting on this correlation id.
            queue_.put(msg)

        self._corr_id_callbacks.pop(  # pylint: disable=protected-access
            correlation_id, None
        )

class MessageNameCallbackInfo(object):
    """
    Data that is used for each registered callback that is based on
    message name.

    Used by :class:`MessageSubscriber`.
    """
    def __init__(self, callback=None, explicit_ack=None):
        """
        :param callback: The callback to invoke. This
            is a callable object or function that takes one argument of type
            :class:`systemlink.messagebus.generic_message.GenericMessage`.
        :type callback: callable
        :param explicit_ack: If ``True``, it means that the ``callback`` is
            responsible for acknowledging the message. If ``False``, it means
            that this Message Subscriber is responsible for acknowledging the
            message (if the
            :class:`systemlink.messagebus.message_subsciber_builder.MessageSubscriberBuilder`
            object used to create this object has enabled explicit
            acknowledgements).
        :type explicit_ack: bool
        """
        self._callback = callback
        self._explicit_ack = explicit_ack

    @property
    def callback(self):
        """
        Get the callback object.

        :return: The callback to invoke. This
            is a callable object or function that takes one argument of type
            :class:`systemlink.messagebus.generic_message.GenericMessage`.
        :rtype: callable
        """
        return self._callback

    @callback.setter
    def callback(self, callback):
        """
        Set the callback object.

        :param callback: The callback to invoke. This
            is a callable object or function that takes one argument of type
            :class:`systemlink.messagebus.generic_message.GenericMessage`.
        :type callback: callable
        """
        self._callback = callback

    @property
    def explicit_ack(self):
        """
        Get the explicit acknowledge mode.

        :return: If ``True``, it means that the ``callback`` is
            responsible for acknowledging the message. If ``False``, it means
            that this Message Subscriber is responsible for acknowledging the
            message (if the
            :class:`systemlink.messagebus.message_subsciber_builder.MessageSubscriberBuilder`
            object used to create this object has enabled explicit
            acknowledgements).
        :rtype: bool
        """
        return self._explicit_ack

    @explicit_ack.setter
    def explicit_ack(self, explicit_ack):
        """
        Set the explicit acknowledge mode.

        :param explicit_ack: If ``True``, it means that the ``callback`` is
            responsible for acknowledging the message. If ``False``, it means
            that this Message Subscriber is responsible for acknowledging the
            message (if the
            :class:`systemlink.messagebus.message_subsciber_builder.MessageSubscriberBuilder`
            object used to create this object has enabled explicit
            acknowledgements).
        :type explicit_ack: bool
        """
        self._explicit_ack = explicit_ack


class CorrIdCallbackInfo(object):
    """
    Data that is used for each registered callback that is based on
    correlation ID.

    Used by :class:`MessageSubscriber`.
    """
    def __init__(self, callback=None, state=None):
        """
        :param callback: The callback to invoke. This
            is a callable object or function that takes one argument of type
            :class:`systemlink.messagebus.generic_message.GenericMessage`.
        :type callback: callable
        :param state: Optional user specific data. May be any
            type.
        :type state: object or None
        """
        self._callback = callback
        self._state = state
        if USE_MONOTONIC_CLOCK:
            self._timestamp = time.monotonic()  # pylint: disable=no-member
        else:
            self._timestamp = datetime.datetime.utcnow()

    @property
    def callback(self):
        """
        Get the callback object.

        :return: The callback to invoke. This
            is a callable object or function that takes one argument of type
            :class:`systemlink.messagebus.generic_message.GenericMessage`.
        :rtype: callable
        """
        return self._callback

    @callback.setter
    def callback(self, callback):
        """
        Set the callback object.

        :param callback: The callback to invoke. This
            is a callable object or function that takes one argument of type
            :class:`systemlink.messagebus.generic_message.GenericMessage`.
        :type callback: callable
        """
        self._callback = callback

    @property
    def state(self):
        """
        Get the ``state`` (optional user specific data).

        :return: Optional user specific data. May be any
            type.
        :rtype: object or None
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Set the ``state`` (optional user specific data).

        :param state: Optional user specific data. May be any
            type.
        :type state: object or None
        """
        self._state = state

    @property
    def timestamp(self):
        """
        Get the timestamp for this object. It is initially set when
        this object is created.

        :return: The timestamp for this object. It is based on an internal
            monotonic clock value.
        :rtype: float
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """
        Set the timestamp for this object.

        :param timestamp: The timestamp for this object. It is based on an internal
            monotonic clock value.
        :type timestamp: float
        """
        self._timestamp = timestamp


class SynchCallbackInfo(object):  # pylint: disable=too-few-public-methods
    """
    Data that is used when a synchronous query is used.

    Used by :class:`systemlink.messagebus.message_service.MessageService`.
    """
    def __init__(self, queue_=None):
        """
        :param queue_: The queue to use for synchronous callbacks. May be
            ``None``.
        :type queue_: queue.Queue or None
        """
        self._queue = queue_

    @property
    def queue(self):
        """
        Get the queue to use for synchronous callbacks.

        :return: The queue to use for synchronous callbacks. May be
            ``None``.
        :rtype: queue.Queue or None
        """
        return self._queue

    @queue.setter
    def queue(self, queue_):
        """
        Set the queue to use for synchronous callbacks.

        :param queue_: The queue to use for synchronous callbacks. May be
            ``None``.
        :type queue_: queue.Queue or None
        """
        self._queue = queue_
