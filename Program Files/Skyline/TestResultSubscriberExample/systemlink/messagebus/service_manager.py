# -*- coding: utf-8 -*-
"""
Service Manager related functions
"""

from __future__ import absolute_import, print_function

# Import python libs
import os.path
import subprocess

# Import local libs
# pylint: disable=import-error
from systemlink.messagebus import service_manager_messages  # pylint: disable=no-name-in-module
from systemlink.messagebus import utils
from systemlink.messagebus.amqp_connection_manager import AmqpConnectionManager
from systemlink.messagebus.exceptions import SystemLinkException
from systemlink.messagebus.message_service import MessageService
from systemlink.messagebus.message_service_builder import MessageServiceBuilder
# pylint: enable=import-error

if utils.is_windows():
    from win32com.shell import shellcon, shell  # pylint: disable=no-name-in-module, import-error


WINDOWS_SERVICE_NAME = 'NI Skyline Service Manager'
SC_EXE_RETCODE_ALREADY_RUNNING = 1056
NET_EXE_RETCODE_ALREADY_STOPPED = 2


def start_service_manager(silent=False):
    """
    Start the NI Skyline Service Manager.

    :param silent: If ``False``, will print status to stdout/stderr.
        If ``True``, will not print status.
    :type silent: bool
    :return: ``True`` if the NI Skyline Service Manager was successfully
        started. ``False`` if the NI Skyline Service Manager was already
        running.
    :rtype: bool
    """
    if not utils.is_windows():
        msg = 'This operation is currently only supported in Windows'
        if not silent:
            utils.eprint(msg)
        raise NotImplementedError(msg)

    sysdir = shell.SHGetFolderPath(
        0, shellcon.CSIDL_SYSTEM, 0, 0
    )
    sc_exe = os.path.join(sysdir, 'sc.exe')
    if not silent:
        print('Starting NI Skyline Service Manager')
    retcode = subprocess.call([sc_exe, 'start', WINDOWS_SERVICE_NAME])
    if retcode == SC_EXE_RETCODE_ALREADY_RUNNING:
        if not silent:
            print('NI Skyline Service Manager already running')
        return False
    if retcode != 0:
        msg = ('Failed to start the NI Skyline Service Manager '
               'with return code {0}'.format(retcode))
        if not silent:
            utils.eprint(msg)
        raise OSError(msg)
    if not silent:
        print('NI Skyline Service Manager successfully started')
    return True


def stop_service_manager(silent=False):
    """
    Stop the NI Skyline Service Manager.

    :param silent: If ``False``, will print status to stdout/stderr.
        If ``True``, will not print status.
    :type silent: bool
    :return: ``True`` if the NI Skyline Service Manager was successfully
        stopped. ``False`` if the NI Skyline Service Manager was already
        stopped.
    :rtype: bool
    """
    if not utils.is_windows():
        msg = 'This operation is currently only supported in Windows'
        if not silent:
            utils.eprint(msg)
        raise NotImplementedError(msg)

    sysdir = shell.SHGetFolderPath(
        0, shellcon.CSIDL_SYSTEM, 0, 0
    )
    net_exe = os.path.join(sysdir, 'net.exe')
    if not silent:
        print('Stopping NI Skyline Service Manager')
    retcode = subprocess.call([net_exe, 'stop', WINDOWS_SERVICE_NAME, '/y'])
    if retcode == NET_EXE_RETCODE_ALREADY_STOPPED:
        if not silent:
            print('NI Skyline Service Manager already stopped')
        return False
    if retcode != 0:
        msg = ('Failed to stop the NI Skyline Service Manager '
               'with return code {0}'.format(retcode))
        if not silent:
            utils.eprint(msg)
        raise OSError(msg)
    if not silent:
        print('NI Skyline Service Manager successfully started')
    return True


def restart_service_manager(silent=False):
    """
    Restart the NI Skyline Service Manager.

    :param silent: If ``False``, will print status to stdout/stderr.
        If ``True``, will not print status.
    :type silent: bool
    """
    stop_service_manager(silent=silent)
    start_service_manager(silent=silent)


def get_services(message_service=None):
    """
    Get information for all services.

    :param message_service: An instance of
        :class:`systemlink.messagebus.message_service.MessageService`.
        May be ``None`` in which case a temporary instance will be
        used.
    :type message_service: systemlink.messagebus.message_service.MessageService
        or None
    :return: A list of service information.
    :rtype:
        list(systemlink.messagebus.service_manager_messages.ServiceInstanceBase)
    """
    if message_service:
        own_message_service = False
    else:
        own_message_service = True
        connection_manager = AmqpConnectionManager()
        builder = MessageServiceBuilder('ServiceManagerClient')
        builder.connection_manager = connection_manager
        message_service = MessageService(builder)

    try:
        request = service_manager_messages.SvcMgrGetServiceInfoSnapshotRequest()
        generic_message = message_service.publish_synchronous_message(request)
        if generic_message is None:
            raise SystemLinkException.from_name('Skyline.RequestTimedOut')
        if generic_message.has_error():
            raise SystemLinkException(error=generic_message.error)

        response = service_manager_messages.SvcMgrGetServiceInfoSnapshotResponse.from_message(
            generic_message
        )
        return response.services
    finally:
        if own_message_service:
            message_service.close()
            message_service = None
            connection_manager.close()
            connection_manager = None


def start_service(service_name, message_service=None):
    """
    Start a specific service.

    :param service_name: The name of the service.
    :type service_name: str
    :param message_service: An instance of
        :class:`systemlink.messagebus.message_service.MessageService`.
        May be ``None`` in which case a temporary instance will be
        used.
    :type message_service: systemlink.messagebus.message_service.MessageService
        or None
    :param silent: If ``False``, will print status to stdout/stderr.
        If ``True``, will not print status.
    :type silent: bool
    """
    if message_service:
        own_message_service = False
    else:
        own_message_service = True
        connection_manager = AmqpConnectionManager()
        builder = MessageServiceBuilder('ServiceManagerClient')
        builder.connection_manager = connection_manager
        message_service = MessageService(builder)

    try:
        node_name = None
        services = get_services(message_service=message_service)
        for service in services:  # pylint: disable=not-an-iterable
            if service.name == service_name:
                node_name = service.node_name
                break

        if node_name is None:
            error_info = 'Service name "{0}" not found.'.format(service_name)
            raise SystemLinkException.from_name('Skyline.Exception', info=error_info)

        broadcast = service_manager_messages.SvcMgrStartServicesBroadcast(
            False,
            [node_name],
            False,
            [service_name],
            1
        )
        message_service.publish_broadcast(broadcast)
    finally:
        if own_message_service:
            message_service.close()
            message_service = None
            connection_manager.close()
            connection_manager = None


def stop_service(service_name, kill=False, message_service=None):
    """
    Stop a specific service.

    :param service_name: The name of the service.
    :type service_name: str
    :param kill: ``True`` to force the service to stop. ``False`` to
        gently inform the service that it should stop.
    :type kill: bool
    :param message_service: An instance of
        :class:`systemlink.messagebus.message_service.MessageService`.
        May be ``None`` in which case a temporary instance will be
        used.
    :type message_service: systemlink.messagebus.message_service.MessageService
        or None
    """
    if message_service:
        own_message_service = False
    else:
        own_message_service = True
        connection_manager = AmqpConnectionManager()
        builder = MessageServiceBuilder('ServiceManagerClient')
        builder.connection_manager = connection_manager
        message_service = MessageService(builder)

    try:
        broadcast = service_manager_messages.SvcMgrStopMultipleServicesBroadcast(
            service_name,
            '',
            kill
        )
        message_service.publish_broadcast(broadcast)
    finally:
        if own_message_service:
            message_service.close()
            message_service = None
            connection_manager.close()
            connection_manager = None
