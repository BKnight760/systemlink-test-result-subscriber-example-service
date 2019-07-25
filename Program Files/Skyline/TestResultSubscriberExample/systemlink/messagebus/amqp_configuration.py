# -*- coding: utf-8 -*-
"""
Implementation of 'AmqpConfiguration' class
"""
from __future__ import absolute_import

# Import python libs
import codecs
import json
import os.path

SKYLINE_LOCALHOST_CONFIGURATION_ID = 'skyline_localhost'
SKYLINE_MASTER_CONFIGURATION_ID = 'skyline_master'


class AmqpConfiguration(object):
    """
    Configuration for an AMQP Connection.
    """
    def __init__(self, filename=None, skyline_configuration=None,
                 last_modified_time=None):
        """
        :param filename: The path to the file that contains the AMQP
            configuration.
        :type filename: str or None
        :param skyline_configuration: The dictionary containing the
            configuration settings for an AMQP connection.
        :type skyline_configuration: dict or None
        :param last_modified_time: The last modified time of the
            AMQP configuration file. This is given as the number
            of seconds since the epoch (epoch is designated by the
             operating system).
        :type last_modified_time: float or None
        """
        self._filename = filename
        if skyline_configuration:
            self._skyline_configuration = skyline_configuration
        else:
            self._skyline_configuration = {}
        self._last_modified_time = last_modified_time

    def refresh(self, force=False):
        """
        If the configuration file changed, refresh the configuration.

        :param force: Force a refresh even if the file has not changed.
        :type force: bool
        :return: ``True`` if the configuration has changed. ``False`` otherwise.
        :rtype: bool
        """
        if not self._filename:
            return False
        last_modified_time = os.path.getmtime(self._filename)
        if not force and self._last_modified_time == last_modified_time:
            return False

        with codecs.open(self._filename, 'r', encoding='utf-8-sig') as fp_:
            configuration = json.loads(fp_.read())

        if not configuration:
            configuration = {}

        self._skyline_configuration = configuration
        self._last_modified_time = last_modified_time
        return True

    @property
    def connection_type(self):
        """
        Get the connection type. Examples are "Local" and "Master".

        :return: The connection type.
        :rtype: str or None
        """
        return self._skyline_configuration.get('ConnectionType', None)

    @connection_type.setter
    def connection_type(self, connection_type):
        """
        Set the connection type. Examples are "Local" and "Master".

        :param connection_type: The connection type.
        :type connection_type: str or None
        """
        self._skyline_configuration['ConnectionType'] = connection_type

    @property
    def exchange_name(self):
        """
        Get the exchange name. An example is "niskyline".

        :return: The exchange name.
        :rtype: str or None
        """
        return self._skyline_configuration.get('ExchangeName', None)

    @exchange_name.setter
    def exchange_name(self, exchange_name):
        """
        Set the exchange name. An example is "niskyline".

        :param exchange_name: The exchange name.
        :type exchange_name: str or None
        """
        self._skyline_configuration['ExchangeName'] = exchange_name

    @property
    def host(self):
        """
        Get the host. Examples are "localhost" and "servername.domain.com".

        :return: The host.
        :rtype: str or None
        """
        return self._skyline_configuration.get('Host', None)

    @host.setter
    def host(self, host):
        """
        Set the host. Examples are "localhost" and "servername.domain.com".

        :param host: The host.
        :type host: str or None
        """
        self._skyline_configuration['Host'] = host

    @property
    def port(self):
        """
        Get the port. An example is 5673.

        :return: The port.
        :rtype: int or None
        """
        return self._skyline_configuration.get('Port', None)

    @port.setter
    def port(self, port):
        """
        Set the port. An example is 5673.

        :param port: The port.
        :type port: int or None
        """
        self._skyline_configuration['Port'] = port

    @property
    def user(self):
        """
        Get the user name. An example is "niskyline".

        :return: The user name.
        :rtype: str or None
        """
        return self._skyline_configuration.get('User', None)

    @user.setter
    def user(self, user):
        """
        Set the user name. An example is "niskyline".

        :param user: The user name.
        :type user: str or None
        """
        self._skyline_configuration['User'] = user

    @property
    def password(self):
        """
        Get the password.

        :return: The password.
        :rtype: str or None
        """
        return self._skyline_configuration.get('Password', None)

    @password.setter
    def password(self, password):
        """
        Set the password.

        :param password: The password.
        :type password: str or None
        """
        self._skyline_configuration['Password'] = password

    @property
    def use_tls(self):
        """
        Get whether TLS is to be used.

        :return: ``True`` if TLS is to be used, ``False`` otherwise.
        :rtype: bool or None
        """
        return self._skyline_configuration.get('UseTls', None)

    @use_tls.setter
    def use_tls(self, use_tls):
        """
        Set whether TLS is to be used.

        :param use_tls: ``True`` if TLS is to be used, ``False`` otherwise.
        :type use_tls: bool or None
        """
        self._skyline_configuration['UseTls'] = use_tls

    @property
    def tls_server_name(self):
        """
        Get the TLS server name. Examples are "localhost" and
        "servername.domain.com".

        :return: The TLS server name.
        :rtype: str or None
        """
        return self._skyline_configuration.get('TlsServerName', None)

    @tls_server_name.setter
    def tls_server_name(self, tls_server_name):
        """
        Set the TLS server name. Examples are "localhost" and
        "servername.domain.com".

        :param tls_server_name: The TLS server name.
        :type tls_server_name: str or None
        """
        self._skyline_configuration['TlsServerName'] = tls_server_name

    @property
    def cert_path(self):
        """
        Get the path to the certificate file. This is a relative path based from
        the Skyline Certificates directory.

        :return: The path to the certificate file.
        :rtype: str or None
        """
        return self._skyline_configuration.get('CertPath', None)

    @cert_path.setter
    def cert_path(self, cert_path):
        """
        Set the path to the certificate file. This is a relative path based from
        the Skyline Certificates directory.

        :param cert_path: The path to the certificate file.
        :type cert_path: str or None
        """
        self._skyline_configuration['CertPath'] = cert_path
