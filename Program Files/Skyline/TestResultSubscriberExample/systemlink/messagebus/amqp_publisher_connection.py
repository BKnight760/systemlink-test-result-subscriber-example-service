# -*- coding: utf-8 -*-
"""
Implementation of 'AmqpPublisherConnection' class
"""
from __future__ import absolute_import

# Import python libs

# Import local libs
# pylint: disable=import-error
from systemlink.messagebus.amqp_connection import AmqpConnection
# pylint: enable=import-error


class AmqpPublisherConnection(AmqpConnection):  # pylint: disable=too-many-instance-attributes
    """
    AMQP Publisher Connection.

    A connection that is used only for publishing (sending)
    messages (and maintaining heartbeats).
    """
    def __init__(self,  # pylint: disable=useless-super-delegation,too-many-arguments
                 amqp_connection_manager,
                 user_name,
                 password,
                 host_name,
                 port,
                 exchange_name,
                 use_tls,
                 tls_server_name,
                 cert_path,
                 timeout_seconds,
                 auto_reconnect=True):
        """
        :param amqp_connection_manager: A
            :class:`systemlink.messagebus.amqp_connection_manager.AmqpConnectionManager`
            object.
        :type amqp_connection_manager:
            systemlink.messagebus.amqp_connection_manager.AmqpConnectionManager
        :param user_name: The user name for the connection.
        :type user_name: str
        :param password: The password for the connection.
        :type password: str
        :param host_name: The hostname for the connection.
        :type host_name: str
        :param port: The port for the connection.
        :type port: int
        :param exchange_name: The exchange name for the connection.
        :type exchange_name: str
        :param use_tls: If ``True``, use TLS for the connection.
        :type use_tls: bool
        :param tls_server_name: The TLS server name for the connection.
        :type tls_server_name: str
        :param cert_path: The certificate path. May be absolute or relative
            to the Skyline Certificates directory.
        :type cert_path: str
        :param timeout_seconds: The connection timeout in seconds.
        :type timeout_seconds: int or float
        :param auto_reconnect: If ``True``, will attempt to reconnect the AMQP connection when
            a disconnect is detected.
        :type auto_reconnect: bool
        """
        super(AmqpPublisherConnection, self).__init__(
            amqp_connection_manager,
            user_name,
            password,
            host_name,
            port,
            exchange_name,
            use_tls,
            tls_server_name,
            cert_path,
            timeout_seconds,
            auto_reconnect=auto_reconnect
        )
        self._heartbeat_only = True
