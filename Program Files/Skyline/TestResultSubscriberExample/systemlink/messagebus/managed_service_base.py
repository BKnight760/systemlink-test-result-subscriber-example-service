# -*- coding: utf-8 -*-
"""
Implementation of 'managed_service_base' and related classes
"""
from __future__ import absolute_import

# Import python libs
import codecs
import datetime
import logging
import os
import socket
import sys
import threading

# Import local libs
# pylint: disable=wrong-import-position,import-error,no-name-in-module
from systemlink.messagebus import audit_trail_messages
from systemlink.messagebus import configuration_messages
from systemlink.messagebus import paths
from systemlink.messagebus import service_manager_messages
from systemlink.messagebus.constants import (
    NODE_NAME, SERVICE_GUID, SERVICE_GROUP_NAME, DEFAULT_SERVICE_GROUP_NAME
)
from systemlink.messagebus.error import Error
from systemlink.messagebus.exceptions import SystemLinkException
from systemlink.messagebus.managed_service_builder import ManagedServiceBuilder
from systemlink.messagebus.message_service import MessageService
from systemlink.messagebus.message_service_builder import MessageServiceBuilder
from systemlink.messagebus.message_subscriber import MessageSubscriber
from systemlink.messagebus.message_subscriber_builder import MessageSubscriberBuilder
from systemlink.messagebus.process_logger import ProcessLogger
# pylint: enable=wrong-import-position,import-error,no-name-in-module

# Set up logging
LOGGER = logging.getLogger(__name__)


class ManagedServiceBase(object):  # pylint: disable=too-many-instance-attributes,too-many-public-methods
    """
    Managed Service Base.

    This class is meant to be inherited by a user created object. It
    enables integration with the Skyline Service Manager.
    """
    def __init__(self, service_name, shutdown_event, managed_service_builder=None):  # pylint: disable=too-many-branches,too-many-statements
        """
        :param service_name: The name of the message service. Ignored
            if ``managed_service_builder`` is not ``None``. In this
             case, ``service_name`` may be ``None``.
        :type service_name: str or None
        :param shutdown_event: A :class`threading.Semaphore` instance
            that is released when the Skyline Service Manager requires
            the service to shut down.
        :type shutdown_event: threading.Semaphore
        :param message_service_builder: A
            :class:`systemlink.messagebus.managed_service_builder.ManagedServiceBuilder`
            object used in the construction of this object. May be
            ``None``, in which case ``service_name`` must be set.
        :type message_service_builder:
            systemlink.messagebus.managed_service_builder.ManagedServiceBuilder
            or None
        """
        LOGGER.debug('ManagedServiceBase constructor!')

        if managed_service_builder is None:
            managed_service_builder = ManagedServiceBuilder(service_name)

        if shutdown_event is None:
            error_info = 'Shutdown event cannot be None'
            raise SystemLinkException.from_name('Skyline.Exception', info=error_info)

        self._closing = False
        self._work_subscriber = None
        self._control_subscriber = None
        self._node_name = ''
        self._service_name = None
        self._instance_name = None
        self._shutdown_thread = None
        self._old_stdout = None
        self._old_stderr = None
        self._devnull_fp = None

        if (sys.stdout is None or sys.stderr is None or
                sys.stdout.encoding != 'utf-8' or
                sys.stderr.encoding != 'utf-8'):
            # We will hit this case when the stdout/stderr pipes
            # are closed before creating this process. This is the
            # current behavior of Service Manager. In Python 3.5.x,
            # this will result in `sys.stdout` and `sys.stderr` being
            # None. In Python 3.6.x, this will result in `sys.stdout`
            # and `sys.stderr` being created by Python, but imperfectly
            # such that the encoding is the system encoding (typically
            # 'cp1252') instead of 'utf-8' which will still cause
            # problems. This should be fixed in Python 3.7.x in which
            # case it should create pipes with an encoding of 'utf-8'.
            # Once Python 3.7.x is the minimum supported version, this
            # code may be removed.
            self._old_stdout = sys.stdout
            self._old_stderr = sys.stderr
            self._devnull_fp = open(os.devnull, 'w', encoding='utf-8')
            sys.stdout = self._devnull_fp
            sys.stderr = self._devnull_fp

        self._service_name = managed_service_builder.service_name
        self._status = service_manager_messages.ServiceState(
            service_manager_messages.ServiceState.STARTING
        )
        self._standalone = managed_service_builder.standalone_property

        if not managed_service_builder.instance_name:
            self._instance_name = self.get_unique_instance_name()
        else:
            self._instance_name = managed_service_builder.instance_name

        self._no_configuration_request = managed_service_builder.no_configuration_request

        self._service_guid = os.environ.get(SERVICE_GUID)
        if not self._service_guid:
            self._service_guid = ''

        self._service_group_name = os.environ.get(SERVICE_GROUP_NAME)
        if not self._service_group_name:
            self._service_group_name = DEFAULT_SERVICE_GROUP_NAME

        if not self._standalone:
            message_subscriber_builder = MessageSubscriberBuilder(self.control_queue_name)
            message_subscriber_builder.callback = self._control_message_callback
            message_subscriber_builder.register_default_binding = True
            message_subscriber_builder.auto_start_consumers = False
            self._control_subscriber = MessageSubscriber(message_subscriber_builder)
            self._control_subscriber.register_callback(
                service_manager_messages.SvcMgrSendServiceStatusRequestBroadcast,
                self._control_message_callback)
            self._control_subscriber.register_callback(
                configuration_messages.ConfigurationGetSectionKeyValuesResponse,
                self._control_message_callback)

        if not managed_service_builder.no_work_subscriber:
            if managed_service_builder.work_subscriber_builder:
                work_builder = managed_service_builder.work_subscriber_builder
            else:
                work_builder = MessageSubscriberBuilder(self._service_name)

            if work_builder.callback is None:
                work_builder.callback = self._receive_message
            work_builder.auto_start_consumers = False
            self._work_subscriber = MessageSubscriber(work_builder)

        if managed_service_builder.instance_subscriber_builder is not None:
            instance_builder = managed_service_builder.instance_subscriber_builder
        else:
            instance_builder = MessageSubscriberBuilder(self.get_full_name())

        instance_builder.register_default_binding = True
        instance_builder.auto_start_consumers = False

        message_service_builder = MessageServiceBuilder(self._service_name)
        message_service_builder.instance_name = self._instance_name
        message_service_builder.subscriber_builder = instance_builder

        self._message_service = MessageService(message_service_builder=message_service_builder)
        self._message_service.instance_name = self._instance_name

        self._process_logger = ProcessLogger(
            self.get_full_name(),
            None,
            self._message_service.publisher.publish_message_callback,
            self._message_service.register_callback)

        log_to_trace_logger = managed_service_builder.log_to_trace_logger
        self._message_service.trace_logger = (
            self._process_logger.make_trace_logger(
                self._service_name, log_to_trace_logger=log_to_trace_logger
            )
        )

        if self._control_subscriber is not None:
            self._control_subscriber.trace_logger = (
                self._process_logger.make_trace_logger(
                    'Control',
                    self._message_service.trace_logger
                )
            )

        if self._work_subscriber is not None:
            self._work_subscriber.trace_logger = self._message_service.trace_logger

        self._trace_unhandled_message = self.trace_logger.make_trace_point('UnhandledMessage')

        self._configured = False
        self._need_to_go_live = False
        self._trace_unhandled_message = None
        self._shutdown_event = shutdown_event
        self._shutdown_thread = None

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        """
        Close this instance of :class:`ManagedServiceBase`.
        """
        if self._closing:
            return
        self._closing = True
        self._wait_on_shutdown_thread()
        if self._work_subscriber is not None:
            self._work_subscriber.close()
        if self._control_subscriber is not None:
            self._control_subscriber.close()
        if self._message_service is not None:
            self._message_service.close()
        if self._devnull_fp is not None:
            sys.stdout = self._old_stdout
            sys.stderr = self._old_stderr
            self._devnull_fp.close()
            self._devnull_fp = None
            self._old_stdout = None
            self._old_stderr = None

    @property
    def service_guid(self):
        """
        Get the GUID (globally unique identifier) used for this service.

        :return: The GUID (globally unique identifier) used for this
            service.
        :rtype: str
        """
        return self._service_guid

    @service_guid.setter
    def service_guid(self, service_guid):
        """
        Set the GUID (globally unique identifier) used for this service.

        :param service_guid: The GUID (globally unique identifier) used
            for this service.
        :type service_guid: str
        """
        self._service_guid = service_guid

    @property
    def service_group_name(self):
        """
        Get the service group name.

        :return: the service group name.
        :rtype: str
        """
        return self._service_group_name

    @service_group_name.setter
    def service_group_name(self, service_group_name):
        """
        Set the service group name.

        :param service_group_name: the service group name.
        :type service_group_name: str
        """
        self._service_group_name = service_group_name

    @staticmethod
    def get_unique_instance_name():
        """
        Generate a unique instance name.

        :return: A unique instance name.
        :rtype: str
        """
        return MessageService.get_unique_instance_name()

    def get_full_name(self, service_name=None, instance_name=None):
        """
        Get the full name based on service name and instance name if
        it exists.

        :param service_name: The name of the message service. If
            ``None``, will use the service name from this instance
            of class:`ManagedServiceBase`.
        :type service_name: str or None
        :param instance_name: The name of the message service instance.
            If ``None``, will use the instance name from this instance
            of class:`ManagedServiceBase`. Both may be ``None`` if
            there is only one instance of the service.
        :type instance_name: str or None
        :return: The full name.
        :rtype: str
        """
        if service_name is None:
            service_name = self._service_name
        if instance_name is None:
            instance_name = self._instance_name
        return MessageService.get_full_name(service_name=service_name, instance_name=instance_name)

    @property
    def host_name(self):
        """
        Get the hostname of this machine.

        :return: The hostname of this machine.
        :rtype: str
        """
        return socket.gethostname()

    @property
    def node_name(self):
        """
        Get the node name of the Service Manager instance that this
        service will use.

        :return: The node name of the Service Manager instance that this
            service will use.
        :rtype: str
        """
        if not self._node_name:
            node_name = ''
            try:
                node_name = os.environ[NODE_NAME]
            except KeyError:
                pass
            if node_name != '':
                self._node_name = node_name.lower()
            else:
                name = self.host_name.lower()
                config_dir = paths.get_configuration_directory()
                node_name_config_path = os.path.join('/', config_dir, 'NodeName.txt')
                try:
                    with codecs.open(node_name_config_path, 'r', encoding='utf-8-sig') as fp_:
                        file_contents = fp_.read().lower()
                        if file_contents is not None and file_contents != 'localhost':
                            name = file_contents
                except IOError:
                    pass
                self._node_name = name
        return self._node_name

    @node_name.setter
    def node_name(self, node_name):
        """
        Set the node name of the Service Manager instance that this
        service will use.

        :param node_name: The node name of the Service Manager instance
             that this service will use.
        :type node_name: str
        """
        self._node_name = node_name

    @property
    def service_name(self):
        """
        Get the service name.

        :return: The service name.
        :rtype: str
        """
        return self._service_name

    @service_name.setter
    def service_name(self, service_name):
        """
        Set the service name.

        :param service_name: The service name.
        :type service_name: str
        """
        self._service_name = service_name

    @property
    def instance_name(self):
        """
        Get the instance name.

        :return: The instance name. May be ``None``.
        :rtype: str or None
        """
        return self._instance_name

    @instance_name.setter
    def instance_name(self, instance_name):
        """
        Set the instance name.

        :param instance_name: The instance name. May be ``None``.
        :type instance_name: str or None
        """
        self._instance_name = instance_name

    @property
    def trace_logger(self):
        """
        Get the Trace Logger.

        :return: The Trace Logger. May be ``None``.
        :rtype: systemlink.messagebus.trace_logger.TraceLogger or None
        """
        return self._message_service.trace_logger

    def make_trace_logger(self, name):
        """
        Create an instance of
        :class:`systemlink.messagebus.trace_logger.TraceLogger`.

        :param name: The last part of the name to use for this Trace Logger.
            Will not be the full name if there is an instance of
            :class:`systemlink.messagebus.trace_logger.TraceLogger`
            associated with this instance of :class:`ManagedServiceBase`.
            In that case, the name of that Trace Logger will be used as
            the parent name (the second last part of the name).
        :type name: str
        :return: A new instance of
            :class:`systemlink.messagebus.trace_logger.TraceLogger`.
        :rtype: systemlink.messagebus.trace_logger.TraceLogger
        """
        return self._process_logger.make_trace_logger(name, self.trace_logger)

    @property
    def current_state(self):
        """
        Get the current state of the service.

        :return: The current state of the service.
        :rtype: systemlink.messagebus.service_manager_messages.ServiceState
        """
        return self._status

    @current_state.setter
    def current_state(self, service_state):
        """
        Set the current state of the service.

        :param service_state: The current state of the service.
        :type service_state:
            systemlink.messagebus.service_manager_messages.ServiceState
        """
        if self._status.value == service_state.value:
            return
        if self._status.value == service_manager_messages.ServiceState.ERROR \
                and service_state.value != service_manager_messages.ServiceState.STOPPED:
            return

        self._status = service_state

        if self._status.value == service_manager_messages.ServiceState.REGISTERED:
            return
        service_status_broadcast = service_manager_messages.ServiceStatusBroadcast(
            self.node_name,
            self.service_guid,
            self.service_name,
            self.service_group_name,
            self.control_queue_name,
            self.current_state
        )
        self.publish_broadcast(service_status_broadcast)

    @property
    def publisher(self):
        """
        Get the message publisher.

        :return: The message publisher.
        :rtype: systemlink.messagebus.message_publisher.MessagePublisher
        """
        return self._message_service.publisher

    @property
    def work_subscriber(self):
        """
        Get the message subscriber for work-related messages.

        :return: The message subscriber for work-related messages.
        :rtype: systemlink.messagebus.message_subscriber.MessageSubscriber
        """
        return self._work_subscriber

    @property
    def instance_subscriber(self):
        """
        Get the message subscriber for messages for this specific
        service instance.

        :return: The message subscriber for messages for this specific
            service instance.
        :rtype: systemlink.messagebus.message_subscriber.MessageSubscriber
        """
        return self._message_service.subscriber

    @property
    def message_service(self):
        """
        Get the associated message service.

        :return: The associated message service.
        :rtype: systemlink.messagebus.message_service.MessageService
        """
        return self._message_service

    @property
    def control_queue_name(self):
        """
        Get the name of the queue used to process control messages
        (messages coming from the Service Manager).

        :return: The name of the queue used to process control messages.
        :rtype: str
        """
        return self.get_full_name(self._service_name, self._instance_name) + '_Control'

    def _register_with_service_manager(self):
        """
        Perform registration with the Service Manager.
        """
        process_id = os.getpid()
        routed_message = \
            service_manager_messages.SvcMgrRegisterLocalServiceRoutedMessage(
                send_to='ServiceManager_' + self.node_name,
                service_guid_=self.service_guid,
                node_name_=self.node_name,
                service_name_=self.service_name,
                service_group_name_=self.service_group_name,
                reply_to_queue_=self.control_queue_name,
                process_id_=process_id
            )
        self.publish_routed_message(routed_message)
        self.current_state = (
            service_manager_messages.ServiceState(service_manager_messages.ServiceState.REGISTERED)
        )

    def _send_service_status_broadcast(self):
        """
        Send the broadcast message that contains service status. It is
        an instance of
        :class:`systemlink.messagebus.service_manager_messages.ServiceStatusBroadcast`.
        """
        service_status_broadcast = service_manager_messages.ServiceStatusBroadcast(
            self.node_name,
            self.service_guid,
            self.service_name,
            self.service_group_name,
            self.control_queue_name,
            self.current_state
        )
        self.publish_routed_message(service_status_broadcast)

    def publish_audit_entry(self, subtype):
        """
        Publish an audit message. It is an instance of
        :class:`systemlink.messagebus.audit_trail_messages.AuditEntry`.

        :param subtype: The audit entry subtype.
        :type subtype: str
        """
        audits = []
        audit_entry = audit_trail_messages.AuditEntry(
            timestamp_=datetime.datetime.utcnow(),
            subtype_=subtype,
            originator_=self.service_name,
            user_name_=None,
            record_type_='Service',
            device_=None,
            detail_=None,
            int1_=0,
            int2_=0,
            int3_=0,
            int4_=0,
            str1_=None,
            str2_=None,
            str3_=None,
            str4_=None
        )
        audits.append(audit_entry)
        audit_add_routed_message = audit_trail_messages.AuditAddRoutedMessage(audits)
        self.publish_routed_message(audit_add_routed_message)

    def _receive_message(self, generic_message):
        """
        The default handler for when a message is received on the work
        or instance queue. Logs an error because it is expected that a
        more specific handler will be registered to handle the message.

        :param generic_message: The incoming message to handle. The
            class of the message is
            :class:`systemlink.messagebus.generic_message.GenericMessage`.
        :type generic_message: systemlink.messagebus.generic_message.GenericMessage
        """
        if generic_message.has_error():
            log_message = (
                'Unhandled message ' +
                generic_message.message_name +
                ': Origin = ' + generic_message.origin +
                ' Error = ' + generic_message.error
            )
            LOGGER.error(log_message)
            self.trace_logger.log_error(log_message, skip_if_has_log_handler=True)
        else:
            log_message = (
                generic_message.message_name +
                ': Origin = ' + generic_message.origin
            )
            LOGGER.error(log_message)
            self.trace_logger.log_error(log_message, skip_if_has_log_handler=True)

    def _try_set_configuration(self, sections):  # pylint: disable=no-self-use,unused-argument
        """
        Not implemented. Always returns success.

        :param sections: A list of key/value pair dictionaries for each
            section in the configuration.
        :type sections: list(systemlink.messagebus.configuration_messages.SectionKeyValues)
        :return: An instance of
            :class:`systemlink.messagebus.error.Error` representing
            the return status of this function.
        :rtype: systemlink.messagebus.error.Error
        """
        # Implement this function when a service needs to perform
        # initialization using the Configuration service.
        # NOTE: This function is called before Message subscriptions
        #       are enabled.
        error = Error()
        return error

    def initialize(self):
        """
        Initialize this instance of :class:`ManagedServiceBase`. Should
        be invoked by the ``__init__`` method of the parent class.

        Supports both standalone and integrated with Service Manager
        use cases.
        """
        if self._standalone:
            self.go_live()
        else:
            self._control_subscriber.start_handling_messages()
            if not self._no_configuration_request:
                request = \
                    configuration_messages.ConfigurationGetSectionKeyValuesRequest()
                request.header.reply_to = self.control_queue_name
                self.publisher.publish_message_base(request)
            else:
                self._configured = True
            self._register_with_service_manager()

    def publish_request(self, request_message):
        """
        Publish a request message.

        :param request_message: The request message.
        :type request_message:
            systemlink.messagebus.request_message.RequestMessage
        """
        self._message_service.publish_request(request_message)

    def publish_response(self, response_message):
        """
        Publish a response message.

        :param response_message: The response message.
        :type response_message:
            systemlink.messagebus.response_message.ResponseMessage
        """
        self._message_service.publish_response(response_message)

    def publish_routed_message(self, routed_message, ignore_response=False):
        """
        Publish a routed message.

        :param routed_message: The routed message.
        :type routed_message:
            systemlink.messagebus.routed_message.RoutedMessage
        :param ignore_response: The ``IgnoreResponse`` property in the
            message header.
        :type ignore_response: bool
        """
        self._message_service.publish_routed_message(routed_message, ignore_response)

    def publish_broadcast(self, broadcast_message):
        """
        Publish a broadcast message.

        :param broadcast_message: The broadcast message.
        :type broadcast_message:
            systemlink.messagebus.broadcast_message.BroadcastMessage
        """
        self._message_service.publish_broadcast(broadcast_message)

    def publish_generic_message(self, generic_message):
        """
        Publish a generic message.

        :param generic_message: The generic message.
        :type generic_message:
            systemlink.messagebus.generic_message.GenericMessage
        """
        self._message_service.publish_generic_message(generic_message)

    def publish_synchronous_message(self, message, mandatory=False, timeout_seconds=None):
        """
        Synchronously publish a message.

        :param message: The message object. The class of this object
            inherits from
            :class:`systemlink.messagebus.message_base.MessageBase`.
        :type message: systemlink.messagebus.message_base.MessageBase
        :param mandatory: The mandatory delivery notification flag.
        :type mandatory: bool
        :param timeout_seconds: The timeout in seconds for this query.
            If ``None``, will use the timeout specified by the
            :class:`systemlink.messagebus.message_service_builder.MessageServiceBuilder`
            object used to create this instance of
            :class:`MessageService`.
        :type timeout_seconds: int or float
        :return: The response message.
        :rtype: systemlink.messagebus.generic_message.GenericMessage
        """
        return self._message_service.publish_synchronous_message(
            message, mandatory=mandatory, timeout_seconds=timeout_seconds
        )

    def publish_generic_response(self, routed_message, error=None):
        """
        Publish a generic response.

        :param request: The request message that is being responded to.
        :type request:
            systemlink.messagebus.routed_message.RoutedMessage
        """
        self._message_service.publish_generic_response(routed_message, error=error)

    def register_work_subscriber_callback(self, message_class_type,  # pylint: disable=invalid-name
                                          callback, message_name=None):
        """
        Register a callback that will be invoked when a
        certain message class type is used.
        Used for work queue messages.

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
        """
        self._work_subscriber.register_callback(
            message_class_type, callback, message_name=message_name
        )

    def register_instance_subscriber_callback(self, message_class_type,  # pylint: disable=invalid-name
                                              callback, message_name=None):
        """
        Register a callback that will be invoked when a
        certain message class type is used.
        Used for instance queue messages.

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
        """
        self._message_service.subscriber.register_callback(
            message_class_type, callback, message_name=message_name
        )

    def go_live(self):
        """
        Notify the Service Manager that this service is live.
        """
        LOGGER.debug('Managed Service Base: go live!')
        process_id = os.getpid()

        log_message = 'Go Live ' + str(process_id) + ' - ' \
                      + self.instance_name \
                      + self.service_name \
                      + ' ServiceGuid='

        if self._standalone:
            log_message += '(Standalone)'
        if self.service_guid:
            log_message += self.service_guid

        self.trace_logger.log_info(log_message)
        self.publish_audit_entry('Live')
        self._message_service.subscriber.start_handling_messages()
        if self._work_subscriber:
            self._work_subscriber.start_handling_messages()
        self.current_state = (
            service_manager_messages.ServiceState(service_manager_messages.ServiceState.LIVE)
        )

    def make_idle(self):
        """
        Notify the Service Manager that this service is idle.
        """
        LOGGER.debug('Managed Service Base: make idle!')
        process_id = os.getpid()

        log_message = (
            'Idled ' + str(process_id) + ' - ' +
            self.instance_name +
            self.service_name +
            ' ServiceGuid='
        )

        if self._standalone:
            log_message += '(Standalone)'
        if self.service_guid:
            log_message += self.service_guid

        self.trace_logger.log_info(log_message)
        self.publish_audit_entry('Idle')
        self._message_service.subscriber.stop_handling_messages()
        if self._work_subscriber:
            self._work_subscriber.stop_handling_messages()
        self.current_state = (
            service_manager_messages.ServiceState(service_manager_messages.ServiceState.IDLE)
        )

    def _shutdown_thread_func(self):
        """
        The thread function for the shutdown thread.

        It will signal the shutdown event and tell the Service Manager
        that it's state is stopped.
        """
        self._shutdown_event.release()
        self.current_state = (
            service_manager_messages.ServiceState(service_manager_messages.ServiceState.STOPPED)
        )

    def _start_shutdown_thread(self):
        """
        Start the shutdown thread if it wasn't already started.
        """
        if self._shutdown_thread is not None:
            return
        self._shutdown_thread = threading.Thread(
            target=self._shutdown_thread_func
        )
        self._shutdown_thread.daemon = True
        self._shutdown_thread.start()

    def _wait_on_shutdown_thread(self):
        """
        Wait for the shutdown thread to complete if it was started.
        """
        if self._shutdown_thread is None:
            return
        self._shutdown_thread.join()
        self._shutdown_thread = None

    def _control_message_callback(self, generic_message):  # pylint: disable=too-many-branches
        """
        The callback function invoked by the framework once a
        control message is received.

        :param generic_message: The response message.
        :type generic_message:
            systemlink.messagebus.generic_message.GenericMessage
        """
        message_name = generic_message.message_name
        LOGGER.debug('Received message: %s', message_name)

        if (message_name ==
                service_manager_messages.SvcMgrSendServiceStatusRequestBroadcast.__name__):
            self._send_service_status_broadcast()  # pylint: disable=protected-access
        elif (message_name ==
              configuration_messages.ConfigurationGetSectionKeyValuesResponse.__name__):
            LOGGER.debug('ConfigurationGetSectionKeyValuesResponse!')
            response = (
                configuration_messages.ConfigurationGetSectionKeyValuesResponse.from_message(
                    generic_message
                )
            )
            error = self._try_set_configuration(  # pylint: disable=protected-access
                response.key_values)
            if error.has_value():
                msg = str(error)
                LOGGER.error(msg)
                self.trace_logger.log_error(
                    msg, skip_if_has_log_handler=True
                )
                self.current_state = (
                    service_manager_messages.ServiceState(
                        service_manager_messages.ServiceState.ERROR
                    )
                )
            else:
                LOGGER.debug('No Error.')
                self._configured = True  # pylint: disable=protected-access
                if self._need_to_go_live:  # pylint: disable=protected-access
                    self.go_live()
        elif message_name == service_manager_messages.ServiceGoLiveRoutedMessage.__name__:
            LOGGER.debug('ServiceGoLiveRoutedMessage')
            service_go_live_routed_message = (
                service_manager_messages.ServiceGoLiveRoutedMessage.from_message(
                    send_to='',
                    message=generic_message
                )
            )
            if not self.service_guid:
                self.service_guid = service_go_live_routed_message.service_guid
            elif (self.service_guid !=
                  service_go_live_routed_message.service_guid):
                log_message = 'Go live request with mis-matched GUID: '
                log_message += self.service_guid
                log_message += " "
                log_message += service_go_live_routed_message.service_guid

                LOGGER.error(log_message)
                self.trace_logger.log_error(
                    log_message, skip_if_has_log_handler=True
                )
            if self.current_state.value \
                    != service_manager_messages.ServiceState.ERROR:
                if self._configured:  # pylint: disable=protected-access
                    self.go_live()
                else:
                    self._need_to_go_live = True  # pylint: disable=protected-access
        elif message_name == service_manager_messages.ServiceMakeIdleRoutedMessage.__name__:
            if (self.current_state !=
                    service_manager_messages.ServiceState.ERROR):
                self._need_to_go_live = False  # pylint: disable=protected-access
                self.make_idle()
        elif message_name == service_manager_messages.ServiceShutdownRoutedMessage.__name__:
            self._start_shutdown_thread()  # pylint: disable=protected-access
        else:
            log_message = 'Unhandled Control Message | '
            log_message += generic_message.message_name
            LOGGER.error(log_message)
            self.trace_logger.log_error(
                log_message, skip_if_has_log_handler=True
            )
