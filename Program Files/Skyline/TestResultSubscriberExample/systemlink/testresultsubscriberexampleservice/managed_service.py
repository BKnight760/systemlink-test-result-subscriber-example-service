# -*- coding: utf-8 -*-
"""
Implementation of the TestResultSubscriberExampleService class.
"""
from __future__ import absolute_import

# Import python libs
import logging
import os.path
import threading
from http import HTTPStatus
from typing import Dict

# Import local libs
# pylint: disable=import-error
from systemlink.messagebus import configuration_messages
from systemlink.messagebus import error
from systemlink.messagebus import error_code_registry
from systemlink.messagebus.amqp_configuration_manager import AmqpConfigurationManager
from systemlink.messagebus.exceptions import SystemLinkException
from systemlink.messagebus.managed_service_base import ManagedServiceBase
from systemlink.messagebus.managed_service_builder import ManagedServiceBuilder
from systemlink.messagebus.paths import get_application_data_directory
from systemlink.testresultsubscriberexampleservice import error_codes
from systemlink.testresultsubscriberexampleservice import loader
# pylint: enable=import-error

# Set up logging
LOGGER = logging.getLogger(__name__)

ERROR_CATEGORY = 'TestResultSubscriberExample'
PLUGIN_CATEGORY_HANDLERS = 'handlers'


class TestResultSubscriberExampleService(ManagedServiceBase):
    """
    Class to publicly access the Test Result Subscriber Example Service.
    """
    def __init__(self, service_name: str, standalone: bool = False):
        """
        :param service_name: The name of the service to use within
            SystemLink.
        :type service_name: str
        :param standalone: Whether or not to run in standalone mode
            (outside of the SystemLink Service Manager).
        :type standalone: bool
        """
        self._config = None
        try:
            builder = ManagedServiceBuilder(service_name)
            builder.standalone_property = standalone
            builder.log_to_trace_logger = True
            builder.no_configuration_request = True
            shutdown_event = threading.Semaphore(0)
            error_codes.register_error_codes()
            super().__init__(
                service_name=None,
                shutdown_event=shutdown_event,
                managed_service_builder=builder)
            # ManagedServiceBase doesn't access the configuration in standalone mode.
            # So we do this ourselves for both standalone and non-standalone modes.
            self._load_config()
            self._register_message_handlers()
            self.initialize()
        except Exception as exc:  # pylint: disable=broad-except
            exc_name = exc.__class__.__name__
            LOGGER.error(
                'Failed to initialize the Test Result Subscriber Example Service. %s: %s',
                exc_name, exc, exc_info=True
            )
            raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def close(self):  # pylint: disable=useless-super-delegation
        """
        Close the TestResultSubscriberExampleService and all associated resources.
        """
        super().close()

    def _register_message_handlers(self):
        """
        Register the message handlers for use with this service.
        """
        plugin_names = loader.get_available_plugins(PLUGIN_CATEGORY_HANDLERS)
        for plugin_name in plugin_names:
            handler_mod = loader.load_plugin(PLUGIN_CATEGORY_HANDLERS, plugin_name)
            handler_mod.register(self)

    @property
    def shutdown_event(self) -> threading.Semaphore:
        """
        Get the shutdown event.

        :return: A :class`threading.Semaphore` instance
            that is released when the SystemLink Service Manager requires
            the service to shut down.
        :rtype: threading.Semaphore
        """
        return self._shutdown_event

    @property
    def config(self) -> Dict[str, str]:
        """
        Get the Test Result Subscriber Example Service configuration.

        :return: A dictionary containing configuration options.
        :rtype: Dict[str, str]
        """
        return self._config

    def _load_config(self):
        """
        Load the Test Result Subscriber Example Service configuration.
        """
        self.message_service.subscriber.start_handling_messages()
        request = configuration_messages.ConfigurationGetKeysRequest(self._service_name)
        generic_response = self.message_service.publish_synchronous_message(request)
        if generic_response is None:
            raise SystemLinkException.from_name(
                'Skyline.UnexpectedException',
                info='Unable to find the configuration for the \"{0}\" service.'.format(
                    self._service_name
                )
            )
        if generic_response.has_error():
            raise SystemLinkException(error=generic_response.error)
        response = configuration_messages.ConfigurationGetKeysResponse.from_message(
            generic_response
        )
        self._config = response.keys
        amqp_config = AmqpConfigurationManager.get_configuration(refresh=False)
        self._config['Amqp.ExchangeName'] = amqp_config.exchange_name
        self._config['Amqp.Host'] = amqp_config.host
        self._config['Amqp.Port'] = str(amqp_config.port)
        self._config['Amqp.User'] = amqp_config.user
        self._config['Amqp.Password'] = amqp_config.password
        if amqp_config.use_tls:
            self._config['Amqp.UseTls'] = 'true'
        else:
            self._config['Amqp.UseTls'] = 'false'
        self._config['Amqp.TlsServerName'] = amqp_config.tls_server_name
        if os.path.isabs(amqp_config.cert_path):
            self._config['Amqp.CertPath'] = amqp_config.cert_path
        else:
            self._config['Amqp.CertPath'] = os.path.join(
                get_application_data_directory(),
                'Certificates',
                amqp_config.cert_path
            )

    def error_response(self, qualified_name, error_args, request_message, response_type,
                       *response_args, **response_kwargs):
        """
        Respond to a request message with an error.

        :param qualified_name: The qualified name of the error. It is in
            the form ``[category].[name]``.
        :type qualified_name: str
        :param error_args: Arguments (if any) for the error code used.
        :type error_args: list or None
        :param request_message: The request message.
        :type request_message:
            systemlink.messagebus.request_message.RequestMessage
        :param response_type: The type of the response message.
        :type response_type: object
        :param response_args: The arguments to initialize the response message
            based on the ``response_type``. Should not include the
            ``request_message``.
        :param response_args: tuple of arguments
        :type response_args: tuple
        :param response_kwargs: dict of arguments
        :type response_kwargs: dict
        """
        if '.' not in qualified_name:
            qualified_name = ERROR_CATEGORY + '.' + qualified_name
        error_code_obj = error_code_registry.lookup(qualified_name)
        error_obj = error.Error(error_code=error_code_obj, args=error_args)
        response_message = response_type(request_message, *response_args, **response_kwargs)
        response_message.error = error_obj
        self.publish_response(response_message)

    def systemlink_exception_response(self, systemlink_exception, request_message, response_type,
                                      *response_args, **response_kwargs):
        """
        Respond to a request message with an error based on a SystemLink Exception.

        :param systemlink_exception: The SystemLink Exception.
        :type systemlink_exception: systemlink.messagebus.exceptions.SystemLinkException
        :param request_message: The request message.
        :type request_message:
            systemlink.messagebus.request_message.RequestMessage
        :param response_type: The type of the response message.
        :type response_type: object
        :param response_args: The arguments to initialize the response message
            based on the ``response_type``. Should not include the
            ``request_message``.
        :param response_args: tuple of arguments
        :type response_args: tuple
        :param response_kwargs: dict of arguments
        :type response_kwargs: dict
        """
        response_message = response_type(request_message, *response_args, **response_kwargs)
        response_message.error = systemlink_exception.error
        self.publish_response(response_message)

    def error_routed(self, qualified_name, error_args, routed_message, response_type,
                     *response_args, **response_kwargs):
        """
        Respond to a routed message with an error.

        :param qualified_name: The qualified name of the error. It is in
            the form ``[category].[name]``.
        :type qualified_name: str
        :param error_args: Arguments (if any) for the error code used.
        :type error_args: list or None
        :param routed_message: An incoming message to handle.
        :type routed_message: systemlink.messagebus.routed_message.RoutedMessage
        :param response_type: The type of the response message.
        :type response_type: object
        :param response_args: The arguments to initialize the response message
            based on the ``response_type``. Should not include the
            ``request_message``.
        :param response_args: tuple of arguments
        :type response_args: tuple
        :param response_kwargs: dict of arguments
        :type response_kwargs: dict
        """
        if '.' not in qualified_name:
            qualified_name = ERROR_CATEGORY + '.' + qualified_name
        error_code_obj = error_code_registry.lookup(qualified_name)
        error_obj = error.Error(error_code=error_code_obj, args=error_args)
        response_message = response_type(routed_message, *response_args, **response_kwargs)
        response_message.error = error_obj
        self.publish_routed_message(response_message)

    def systemlink_exception_routed(self, systemlink_exception, routed_message, response_type,
                                    *response_args, **response_kwargs):
        """
        Respond to a routed message with an error based on a SystemLink Exception.

        :param systemlink_exception: The SystemLink Exception.
        :type systemlink_exception: systemlink.messagebus.exceptions.SystemLinkException
        :param request_message: The request message.
        :type request_message:
            systemlink.messagebus.request_message.RequestMessage
        :param response_type: The type of the response message.
        :type response_type: object
        :param response_args: The arguments to initialize the response message
            based on the ``response_type``. Should not include the
            ``request_message``.
        :param response_args: tuple of arguments
        :type response_args: tuple
        :param response_kwargs: dict of arguments
        :type response_kwargs: dict
        """
        response_message = response_type(routed_message, *response_args, **response_kwargs)
        response_message.error = systemlink_exception.error
        self.publish_routed_message(response_message)
