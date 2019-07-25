# -*- coding: utf-8 -*-
"""
Implementation of 'AmqpConnection' class
"""
from __future__ import absolute_import

# Import python libs
import contextlib
import datetime
import logging
import os
import ssl
import sys
import threading
import time
from binascii import a2b_base64

# Import third party libs
# pylint: disable=import-error
import pika
import pika.spec
import pika.connection
import pika.exceptions
# pylint: enable=import-error

# Import local libs
# pylint: disable=import-error
from systemlink.messagebus.exceptions import SystemLinkException
from systemlink.messagebus.amqp_channel import AmqpChannel, raise_connection_closed
from systemlink.messagebus.message_header import ROUTING_KEY_PREFIX
from systemlink.messagebus.paths import get_base_configuration_directory
if sys.version_info[0] < 3:
    from Queue import Queue
else:
    from queue import Queue
# pylint: enable=import-error

try:
    from asn1crypto.x509 import Certificate
    HAS_ASN1CRYPTO = True
    HAS_PYCRYPTO = False
except ImportError:
    HAS_ASN1CRYPTO = False
    try:
        from Crypto.Util.asn1 import DerSequence
        HAS_PYCRYPTO = True
    except ImportError:
        HAS_PYCRYPTO = False

# Set up logging
LOGGER = logging.getLogger(__name__)


def _der_to_datetime(der_time):
    """
    Change a DER binary encoded UTCTime to a :class:`datetime.datetime` object.
    DER stands for Distinguished Encoding Rules.

    PyCrypto doesn't have logic that parses DER binary encoded times, so
    we do it ourselves here.

    :param der_time: The DER binary encoded UTCTime.
    :type der_time: bytes
    :return: A :class:`datetime.datetime` object that represents the DER
        binary encoded UTCTime.
    :rtype: datetime.datetime
    :raises systemlink.messagebus.exceptions.SystemLinkException: If the conversion
        fails.
    """
    # We expect the DER to start with \x17 which is for UTCTime and then
    # with \x0D (13) which is the length. The length will always be the
    # same because it must be in the format 'YYMMDDHHMMSSZ'.
    if not der_time.startswith(b'\x17\x0D'):
        error_info = 'Unable to decode certificate UTCTime. Unexpected header.'
        raise SystemLinkException.from_name('Skyline.Exception', info=error_info)

    if sys.version_info[0] < 3:
        datetime_string = der_time[2:]
    else:
        datetime_string = der_time[2:].decode('utf-8')

    # From the spec [https://www.ietf.org/rfc/rfc3280.txt]:
    #     Where YY is greater than or equal to 50, the year SHALL be
    #     interpreted as 19YY; and
    #
    #     Where YY is less than 50, the year SHALL be interpreted as 20YY.
    try:
        year = int(datetime_string[0:2])
    except ValueError:
        error_info = (
            'Unable to decode certificate UTCTime. '
            'Unexpected value: "{0}".'.format(datetime_string)
        )
        raise SystemLinkException.from_name('Skyline.Exception', info=error_info)
    if year >= 50:
        year_prefix = '19'
    else:
        year_prefix = '20'
    adj_datetime_string = year_prefix + datetime_string

    format_str = '%Y%m%d%H%M%SZ'
    try:
        datetime_obj = datetime.datetime.strptime(adj_datetime_string, format_str)
    except ValueError:
        error_info = (
            'Unable to decode certificate UTCTime. '
            'Unexpected value: "{0}".'.format(datetime_string)
        )
        raise SystemLinkException.from_name('Skyline.Exception', info=error_info)
    return datetime_obj


def _check_certificate(cert_abs_path):
    """
    Check the cerficate. Will raise
    :class:`systemlink.messagebus.exceptions.SystemLinkException` with details if
    the certicate check fails.

    :param cert_abs_path: Absolute path to the cerficate file.
    :type cert_abs_path: str
    :raises systemlink.messagebus.exceptions.SystemLinkException: If the certificate
        check fails.
    """
    if not HAS_ASN1CRYPTO and not HAS_PYCRYPTO:
        error_info = 'Cannot import asn1crypto nor PyCrypto[dome] for certificate check.'
        raise SystemLinkException.from_name('Skyline.InternalServiceError', info=error_info)

    with open(cert_abs_path) as fp_:
        pem = fp_.read()
    lines = pem.replace(' ', '').split()
    # Skip over begin and end lines
    der = a2b_base64(''.join(lines[1:-1]))
    # Extract validity field from X.509 certificate (see RFC3280)
    if HAS_ASN1CRYPTO:
        cert = Certificate.load(der)
        tbs_certificate = cert['tbs_certificate']
        validity = tbs_certificate['validity']
        not_before = validity['not_before'].native
        not_before = not_before.replace(tzinfo=None)
        not_after = validity['not_after'].native
        not_after = not_after.replace(tzinfo=None)
    else:
        cert = DerSequence()
        cert.decode(der)
        tbs_certificate = DerSequence()
        tbs_certificate.decode(cert[0])
        validity = DerSequence()
        validity.decode(tbs_certificate[4])
        not_before = _der_to_datetime(validity[0])
        not_after = _der_to_datetime(validity[1])
    now = datetime.datetime.utcnow()
    if now < not_before or now > not_after:
        error_info = (
            'Certificate check failed. Certificate is valid from {0} to {1} (UTC). '
            'Current system UTC time is {2}, which is outside the valid range. '
            'Please ensure that the current system time is properly set.'
            ''.format(not_before, not_after, now)
        )
        raise SystemLinkException.from_name('Skyline.AMQPErrorCertificateExpired', info=error_info)


class AmqpConnection(object):  # pylint: disable=too-many-instance-attributes
    """
    AMQP Connection.
    """
    _exchange_initialized = False

    def __init__(self,  # pylint: disable=too-many-arguments
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
        self._connection_lock = threading.RLock()
        self._state_lock = threading.Lock()
        self._closing = False
        self._connected = False
        self._auto_reconnect = auto_reconnect
        self._reconnect_failures = 0
        self._amqp_connection_manager = amqp_connection_manager
        LOGGER.debug(
            'AmqpConnection\'s amqp_connection_manager: %s',
            self._amqp_connection_manager
        )
        self._user_name = user_name
        self._password = password
        self._host_name = host_name
        self._port = port
        self._exchange_name = exchange_name
        self._use_tls = use_tls
        self._tls_server_name = tls_server_name
        self._cert_path = cert_path
        self._timeout_seconds = timeout_seconds
        self._auto_ack = False
        self._heartbeat_only = False
        self._stop_consuming_event = threading.Event()
        if self._auto_reconnect:
            self._connection_close_event = threading.Event()
        else:
            self._connection_close_event = None
        self._monitoring_thread = None
        self._monitoring_thread_should_stop = False
        self._consumer_thread = None
        self._consumer_thread_should_stop = False
        self._connection = None
        self._amqp_channels = {}
        with self._connection_lock:
            self._initialize()
        self._connected = True

    def __del__(self):
        self.close()

    def _initialize(self):
        """
        Used to initialize this :class:`AmqpConsumer` object or re-initialize
        it after a disconnect is detected.
        """
        LOGGER.debug('AmqpConnection _initialize!')
        credentials = pika.PlainCredentials(self._user_name, self._password)
        cert_abs_path = None

        if self._use_tls:
            # Get RabbitMQ server certificate path
            if os.path.isabs(self._cert_path):
                cert_abs_path = self._cert_path
            else:
                cert_abs_path = os.path.join(
                    get_base_configuration_directory(),
                    'Certificates',
                    self._cert_path
                )
            if pika.__version__[0] == '0':
                # Backwards compatibility for pika < 1.0.0.
                ssl_options = {
                    'ssl_version': ssl.PROTOCOL_TLSv1_2,
                    'cert_reqs': ssl.CERT_REQUIRED,
                    'ca_certs': cert_abs_path
                }
                kwargs = {'ssl': True}
            else:
                ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1_2)
                ssl_context.verify_mode = ssl.CERT_REQUIRED
                ssl_context.load_verify_locations(cert_abs_path)
                ssl_options = pika.SSLOptions(ssl_context)
                kwargs = {}
        else:
            ssl_options = None
            kwargs = {}

        conn_params = pika.ConnectionParameters(
            host=self._host_name,
            port=self._port,
            credentials=credentials,
            ssl_options=ssl_options,
            **kwargs
        )

        try:
            self._connection = pika.BlockingConnection(conn_params)
        except Exception as exc:  # pylint: disable=broad-except
            # This will throw its own exception if it detects a problem.
            if cert_abs_path:
                _check_certificate(cert_abs_path)
            # Throw a generic exception since we don't know what the specific
            # problem is.
            exc_name = exc.__class__.__name__
            exc_str = str(exc)
            if exc_str:
                msg = 'Error connecting to AMQP. {0}: {1}'.format(exc_name, exc_str)
            else:
                msg = 'Error connecting to AMQP. {0}'.format(exc_name)
            raise SystemLinkException.from_name('Skyline.AMQPErrorOpeningTCPConnection', info=msg)

    @contextlib.contextmanager
    def _convert_error_contextmanager(self, channel=None, default_error_name='Skyline.Exception'):
        """
        A context manager to convert Pika errors to Skyline errors.

        :param channel: If a channel is being used, the channel. Otherwise
            ``None``.
        :type channel: pika.channel.Channel or None
        :param default_error_code: The error code to use if a more
            specific error code cannot be determined.
        :type default_error_code: int
        """
        try:
            yield
        except SystemLinkException:
            raise
        except Exception as orig_exc:  # pylint: disable=broad-except
            # As for AttributeError:
            # We see this sometimes when the socket is closed:
            #
            # File "/usr/lib/python2.7/site-packages/pika/adapters/base_connection.py", line 427,
            #    in _handle_write
            #  bw = self.socket.send(frame)
            # AttributeError: 'NoneType' object has no attribute 'send'
            #
            # In this case, the socket is gone but it is still trying to use it.
            # This could happen if the broker went down.

            # As for ValueError:
            # We see this sometimes when the socket is closed on the consumer:
            #
            # File "c:\...\lib\site-packages\pika\adapters\base_connection.py", line 415, in
            #     _handle_read
            #   data = self.socket.read(self._buffer_size)
            # File "c:\...\lib\ssl.py", line 869, in read
            #   raise ValueError("Read on closed or unwrapped SSL socket.")
            orig_exc_cls = orig_exc.__class__
            orig_exc_name = orig_exc_cls.__name__
            msg = '{0}: {1}'.format(orig_exc_name, orig_exc)
            error_name = default_error_name
            if (issubclass(orig_exc_cls, pika.exceptions.ProbableAuthenticationError) or
                    issubclass(orig_exc_cls, pika.exceptions.AuthenticationError) or
                    issubclass(orig_exc_cls, pika.exceptions.ProbableAccessDeniedError)):
                error_name = 'Skyline.AMQPErrorFailedToLogIn'
            elif issubclass(orig_exc_cls, pika.exceptions.ConsumerCancelled):
                error_name = 'Skyline.AMQPErrorPerformingBasicConsume'
            elif issubclass(orig_exc_cls, pika.exceptions.UnroutableError):
                error_name = 'Skyline.AMQPErrorPublishingMessage'

            if ((channel and channel.is_closed) or  # pylint: disable=too-many-boolean-expressions
                    not self._connection or self._connection.is_closed or
                    issubclass(orig_exc_cls, pika.exceptions.ChannelClosed) or
                    issubclass(orig_exc_cls, pika.exceptions.ConnectionClosed) or
                    issubclass(orig_exc_cls, AttributeError) or
                    issubclass(orig_exc_cls, ValueError)):
                self._connected = False
                if self._auto_reconnect:
                    # Kick off the auto-reconnect functionality.
                    self._connection_close_event.set()

            raise SystemLinkException.from_name(error_name, info=msg)

    def close(self):
        """
        Close this instance of :class:`AmqpConnection`.
        """
        with self._connection_lock:
            if self._closing:
                return
            self._closing = True
            LOGGER.debug('AmqpConnection close!')
            self.stop_consuming(has_connection_lock=True)
            if self._connection is not None:
                reply_code = 200
                reply_text = 'Normal shutdown'
                try:
                    self._connection.close(reply_code, reply_text)
                except Exception as exc:  # pylint: disable=broad-except
                    exc_name = exc.__class__.__name__
                    LOGGER.error(
                        'Error when closing connection. %s: %s',
                        exc_name, exc, exc_info=True
                    )

    def create_channel(self):
        """
        Create a new channel on this connection.

        :return: A :class:`systemlink.messagebus.amqp_channel.AmqpChannel`
            object.
        :rtype: systemlink.messagebus.amqp_channel.AmqpChannel
        """
        cls = self.__class__
        with self._connection_lock:
            if not self._connection:
                raise_connection_closed()
            found_channel_id = 0
            for channel_id in range(1, 32000):
                if channel_id not in self._amqp_channels.keys():
                    LOGGER.debug(
                        'channel_id %d not in keys %s!',
                        channel_id, self._amqp_channels.keys()
                    )
                    with self._convert_error_contextmanager(
                            default_error_name='Skyline.AMQPErrorOpeningChannel'):
                        channel = self._connection.channel(channel_id)

                    queue = Queue()
                    amqp_channel = AmqpChannel(self, channel, channel_id, queue)
                    self._amqp_channels[channel_id] = amqp_channel
                    found_channel_id = channel_id
                    break
            if found_channel_id == 0:
                error_info = 'All channel IDs have been reserved'
                raise SystemLinkException.from_name('Skyline.Exception', info=error_info)
            if self._heartbeat_only and len(self._amqp_channels) == 1:
                self.start_consuming(True)
            LOGGER.debug(
                'AmqpConnection create_channel exchange_initialized = %s',
                cls._exchange_initialized  # pylint: disable=protected-access
            )
            if not cls._exchange_initialized:  # pylint: disable=protected-access
                self.declare_exchange(found_channel_id)
                cls._exchange_initialized = True  # pylint: disable=protected-access
                LOGGER.debug('Setting exchange_initialized: %s', cls._exchange_initialized)  # pylint: disable=protected-access
            return amqp_channel

    def remove_channel(self, amqp_channel):
        """
        Remove a new channel from this connection.

        :param amqp_channel: A :class:`systemlink.messagebus.amqp_channel.AmqpChannel`
            object.
        :type amqp_channel: systemlink.messagebus.amqp_channel.AmqpChannel
        """
        with self._connection_lock:
            if len(self._amqp_channels) == 1:
                self.stop_consuming(has_connection_lock=True)

            found_channel_id = 0
            for channel_id, cur_amqp_channel in self._amqp_channels.items():
                if amqp_channel == cur_amqp_channel:
                    found_channel_id = channel_id
                    break
            if found_channel_id:
                try:
                    amqp_channel.close()
                except pika.exceptions.ChannelClosed:
                    pass
                del self._amqp_channels[found_channel_id]

    def acknowledge_message(self, amqp_channel, delivery_tag):  # pylint: disable=no-self-use
        """
        Acknowledge a message (meaning that it has been processed by this
        consumer).

        :param amqp_channel: A :class:`systemlink.messagebus.amqp_channel.AmqpChannel`
            object.
        :type amqp_channel: systemlink.messagebus.amqp_channel.AmqpChannel
        :param delivery_tag: The message delivery tag.
        :type delivery_tag: str
        """
        if delivery_tag == 0:
            return
        with self._connection_lock:
            if not self._connection or not amqp_channel.channel:
                raise_connection_closed()
            with self._convert_error_contextmanager(
                    amqp_channel.channel,
                    default_error_name='Skyline.Exception'):
                amqp_channel.channel.basic_ack(delivery_tag)

    def not_acknowledge_message(self, amqp_channel, delivery_tag):  # pylint: disable=no-self-use
        """
        Not acknowledge a message (meaning that it will not be processed by
        this consumer).

        :param amqp_channel: A :class:`systemlink.messagebus.amqp_channel.AmqpChannel`
            object.
        :type amqp_channel: systemlink.messagebus.amqp_channel.AmqpChannel
        :param delivery_tag: The message delivery tag.
        :type delivery_tag: str
        """
        if delivery_tag == 0:
            return
        with self._connection_lock:
            if not self._connection or not amqp_channel.channel:
                raise_connection_closed()
            with self._convert_error_contextmanager(
                    amqp_channel.channel,
                    default_error_name='Skyline.Exception'):
                amqp_channel.channel.basic_nack(delivery_tag)

    def register_binding(self, amqp_channel, queue_name, binding_parameters):
        """
        Register a binding.

        :param amqp_channel: A :class:`systemlink.messagebus.amqp_channel.AmqpChannel` object.
        :type amqp_channel: systemlink.messagebus.amqp_channel.AmqpChannel
        :param queue_name: The queue name.
        :type queue_name: str
        :param binding_parameters: A list of strings that represent a routing key.
        :type binding_parameters: list(str)
        """
        binding_key = ROUTING_KEY_PREFIX
        for param in binding_parameters:
            binding_key += '.' + param

        with self._connection_lock:
            if not self._connection or not amqp_channel.channel:
                raise_connection_closed()
            with self._convert_error_contextmanager(
                    amqp_channel.channel,
                    default_error_name='Skyline.AMQPErrorBindingQueue'):
                amqp_queue_bind_ok = amqp_channel.channel.queue_bind(
                    queue_name, self._exchange_name, binding_key
                )
            LOGGER.debug(
                'AmqpConnection register_binding amqp_queue_bind_ok = %s',
                amqp_queue_bind_ok
            )
            LOGGER.debug('amqp_queue_bind_ok.method = %s', amqp_queue_bind_ok.method)

    def unregister_binding(self, amqp_channel, queue_name, binding_parameters):
        """
        Unregister a binding.

        :param amqp_channel: A :class:`systemlink.messagebus.amqp_channel.AmqpChannel` object.
        :type amqp_channel: systemlink.messagebus.amqp_channel.AmqpChannel
        :param queue_name: The queue name.
        :type queue_name: str
        :param binding_parameters: A list of strings that represent a routing key.
        :type binding_parameters: list(str)
        """
        binding_key = ROUTING_KEY_PREFIX

        for param in binding_parameters:
            binding_key += '.' + param

        with self._connection_lock:
            if not self._connection or not amqp_channel.channel:
                raise_connection_closed()
            with self._convert_error_contextmanager(
                    amqp_channel.channel,
                    default_error_name='Skyline.AMQPErrorUnbindingQueue'):
                amqp_rpc_reply = amqp_channel.channel.queue_unbind(
                    queue_name, self._exchange_name, binding_key
                )
            if amqp_rpc_reply != 0:
                error_info = (
                    'Error unbinding queue.'
                    'Channel: {0}. '
                    'Queue name: {1}. '
                    'Exchange name: {2}. '
                    'Binding key: {3}. '
                    'AmqpRPCReply: {4}. '.format(
                        amqp_channel.channel,
                        queue_name,
                        self._exchange_name,
                        binding_key,
                        amqp_rpc_reply
                    )
                )
                raise SystemLinkException.from_name(
                    'Skyline.AMQPErrorUnbindingQueue', info=error_info
                )

    def queue_declare(self, amqp_channel, queue_name, durable, exclusive, autodelete):  # pylint: disable=too-many-arguments
        """
        Declare a queue.

        :param amqp_channel: A :class:`systemlink.messagebus.amqp_channel.AmqpChannel` object.
        :type amqp_channel: systemlink.messagebus.amqp_channel.AmqpChannel
        :param queue_name: The queue name.
        :type queue_name: str
        :param durable: ``True`` if the queue is durable (backed up to
            persistent storage).
        :type durable: bool
        :param exclusive: ``True`` if the queue is exclusive.
        :type exclusive: bool
        :param autodelete: ``True`` is the queue should automatically delete
            itself when it is no longer referenced.
        :type autodelete: bool
        """
        LOGGER.debug('AmqpConnection queue_declare! '
                     'Queue name: %s.', queue_name)
        passive = False

        with self._connection_lock:
            if not self._connection or not amqp_channel.channel:
                raise_connection_closed()
            with self._convert_error_contextmanager(
                    amqp_channel.channel,
                    default_error_name='Skyline.AMQPErrorDeclaringQueue'):
                amqp_queue_declare_ok = amqp_channel.channel.queue_declare(
                    queue=queue_name,
                    passive=passive,
                    durable=durable,
                    exclusive=exclusive,
                    auto_delete=autodelete
                )
            LOGGER.debug('amqp_queue_declare_ok = %s', amqp_queue_declare_ok)
            if amqp_queue_declare_ok.method.queue != queue_name:
                error_info = (
                    'Error declaring queue. '
                    'Channel: {0}. '
                    'Queue name: {1}. '
                    'Durable: {2}. '
                    'Exclusive: {3}. '
                    'Auto delete: {4}. '.format(
                        amqp_channel.channel, queue_name, durable, exclusive, autodelete)
                )

                raise SystemLinkException.from_name('Skyline.AMQPErrorDeclaringQueue', error_info)

    def basic_qos(self, amqp_channel, prefetch_size, prefetch_count, global_qos):  # pylint: disable=too-many-arguments
        """
        Specify quality of service.

        :param amqp_channel: A `systemlink.messagebus.amqp_channel.AmqpChannel` object.
        :type amqp_channel: systemlink.messagebus.amqp_channel.AmqpChannel
        :param prefetch_size: The prefetch window size. ``0`` means no
            specific limit.
        :type prefetch_size: int
        :param prefetch_count: Specifies a prefetch window in terms of
            whole messages.
        :type prefetch_count: int
        :param global_qos: ``True`` if the QoS should apply to all
            consumers on the channel. ``False`` if the QoS should
            apply only to this consumer.
        :type global_qos: bool
        """
        with self._connection_lock:
            if not self._connection or not amqp_channel.channel:
                raise_connection_closed()
            with self._convert_error_contextmanager(
                    amqp_channel.channel,
                    default_error_name='Skyline.AMQPErrorSettingQoS'):
                amqp_basic_qos_ok = amqp_channel.channel.basic_qos(
                    prefetch_size,
                    prefetch_count,
                    global_qos
                )
            LOGGER.debug('amqp_basic_qos_ok = %s', amqp_basic_qos_ok)

    def start_consuming(self, auto_ack):
        """
        Signal the AMQP connection to start consuming messages.

        :param auto_ack: If ``True``, automatic acknowledgement mode
            will be used (see http://www.rabbitmq.com/confirms.html).
            This corresponds to the ``no_ack`` parameter in the
            basic.consume AMQP 0.9.1 method.
        :type auto_ack: bool
        """
        with self._state_lock:
            if self._consumer_thread is None:
                self._auto_ack = auto_ack
                self._consumer_thread_should_stop = False
                self._consumer_thread = threading.Thread(
                    target=self._consumer_thread_func
                )
                self._consumer_thread.daemon = True
                self._consumer_thread.start()
            if self._monitoring_thread is None and self._auto_reconnect:
                self._monitoring_thread_should_stop = False
                self._monitoring_thread = threading.Thread(target=self._monitoring_thread_func)
                self._monitoring_thread.daemon = True
                self._monitoring_thread.start()

    def stop_consuming(self, has_connection_lock=False):  # pylint: disable=too-many-branches
        """
        Signal the AMQP connection to stop consuming messages.

        :param has_connection_lock: ``True`` if the connection lock is already
            being held.
        :type has_connection_lock: bool
        """
        with self._state_lock:
            self._stop_consuming_event.set()
            if self._monitoring_thread is not None:
                self._monitoring_thread_should_stop = True
                self._connection_close_event.set()
                if has_connection_lock:
                    self._connection_lock.release()
                try:
                    self._monitoring_thread.join()
                finally:
                    if has_connection_lock:
                        self._connection_lock.acquire()
                self._monitoring_thread = None
            if self._consumer_thread is not None:
                self._consumer_thread_should_stop = True
                if has_connection_lock:
                    self._connection_lock.release()
                try:
                    self._consumer_thread.join()
                finally:
                    if has_connection_lock:
                        self._connection_lock.acquire()
                self._consumer_thread = None
            self._stop_consuming_event.clear()

    def declare_exchange(self, channel_id):
        """
        Declare an exchange.

        :param channel_id: The channel ID of the AMQP channel to use.
        :type channel_id: int
        """
        LOGGER.debug('AmqpConnection declare_exchange!')
        with self._connection_lock:
            channel = self._amqp_channels[channel_id].channel
            if not self._connection or not channel:
                raise_connection_closed()
            with self._convert_error_contextmanager(
                    channel,
                    default_error_name='Skyline.AMQPErrorDeclaringExchange'):
                channel.exchange_declare(
                    exchange=self._exchange_name,
                    exchange_type='topic',
                    durable=True
                )

    def publish_message(self, amqp_channel, header, body, mandatory):
        """
        Publish a message.

        :param amqp_channel: A `systemlink.messagebus.amqp_channel.AmqpChannel` object.
        :type amqp_channel: systemlink.messagebus.amqp_channel.AmqpChannel
        :param header: A :class:`systemlink.messagebus.message_header.MessageHeader`
            object.
        :type header: systemlink.messagebus.message_header.MessageHeader
        :param body: The message body.
        :type body: bytes
        :param mandatory: If ``True``, the broker will return an unroutable message
            to the sender as a ``Return`` message.
        :type mandatory: bool
        """
        with self._connection_lock:
            if not self._connection or not amqp_channel.channel:
                raise_connection_closed()
            message_type = header.message_name
            LOGGER.debug('message_type = %s', message_type)
            headers = header.properties
            LOGGER.debug('headers = %s', headers)
            correlation_id = header.correlation_id
            LOGGER.debug('correlation_id = %s', correlation_id)
            timestamp = int(time.mktime(header.timestamp.timetuple()))
            LOGGER.debug('timestamp = %s', timestamp)
            if header.persistent:
                delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
            else:
                delivery_mode = None
            LOGGER.debug('delivery_mode = %s', delivery_mode)
            properties = pika.BasicProperties(
                content_type='application/json',
                headers=headers,
                delivery_mode=delivery_mode,
                correlation_id=correlation_id,
                timestamp=timestamp,
                type=message_type
            )
            routing_key = header.routing_key
            LOGGER.debug('exchange = %s', self._exchange_name)
            LOGGER.debug('routing_key = %s', routing_key)
            LOGGER.debug('body = %s', body)
            LOGGER.debug('properties = %s', properties)
            LOGGER.debug('mandatory = %s', mandatory)

            with self._convert_error_contextmanager(
                    amqp_channel.channel,
                    default_error_name='Skyline.AMQPErrorPublishingMessage'):
                amqp_channel.perform_publish(
                    exchange_name=self._exchange_name,
                    routing_key=routing_key,
                    body=body,
                    properties=properties,
                    mandatory=mandatory
                )

    def handle_message_returned(self, correlation_id, message_type):
        """
        Handle the case when a mandatory message was returned.

        :param correlation_id: The correlation ID of the returned message.
        :type correlation_id: str
        :param message_type: The message type of the returned message.
        :type message_type: str
        """
        # There is no way to determine which subscriber may have a synchronous
        # callback registered for this correlation id. Send the event to every
        # queue, and queues that do not have a matching callback will skip
        # processing it.
        with self._connection_lock:
            for amqp_channel in self._amqp_channels.values():
                # Enqueue as a 2-tuple
                amqp_channel.message_returned_queue.put_nowait(
                    (correlation_id, message_type)
                )

    def _monitoring_thread_func(self):  # pylint: disable=too-many-branches
        """
        The thread function for the monitoring thread.

        When a disconnect is detected, it will re-initialize the connection.
        """
        try:
            while True:
                try:
                    self._connection_close_event.wait()
                    LOGGER.debug('AmqpConnection monitoring_thread acquired semaphore!')
                    if self._monitoring_thread_should_stop:
                        break
                    self._connected = False
                    if self._reconnect_failures == 0:
                        # Avoid spamming warnings every reconnect attempt.
                        LOGGER.warning('Attempting to reconnect to AMQP')
                        self._amqp_connection_manager.put_status_message(
                            'Attempting to reconnect to AMQP...', False, replace_if_full=True
                        )
                    with self._connection_lock:
                        if self._monitoring_thread_should_stop:
                            break
                        for amqp_channel in self._amqp_channels.values():
                            if amqp_channel.channel:
                                amqp_channel.cancel_consume()
                                try:
                                    amqp_channel.channel.close()
                                except Exception:  # pylint: disable=broad-except
                                    pass
                                amqp_channel.channel = None
                        if self._connection:
                            try:
                                self._connection.close()
                            except Exception:  # pylint: disable=broad-except
                                pass
                            self._connection = None
                        self._initialize()
                        for amqp_channel in self._amqp_channels.values():
                            with self._convert_error_contextmanager(
                                    default_error_name='Skyline.AMQPErrorOpeningChannel'):
                                amqp_channel.channel = self._connection.channel(
                                    amqp_channel.channel_id
                                )
                            amqp_channel._channel_close_event.release()  # pylint: disable=protected-access
                        self._connected = True
                        self._reconnect_failures = 0
                        self._connection_close_event.clear()
                    # Tell the user that the reconnect was successful
                    # so that they can see that the system is back in a
                    # good state via their error log.
                    LOGGER.error('Reconnect to AMQP successful')
                except Exception as exc:  # pylint: disable=broad-except
                    if not self._monitoring_thread_should_stop:
                        if self._reconnect_failures == 0:
                            exc_name = exc.__class__.__name__
                            LOGGER.error(
                                'Exception when attempting reconnect. %s: %s',
                                exc_name, exc, exc_info=True
                            )
                        self._amqp_connection_manager.exception = exc
                        self._reconnect_failures += 1
                        sleep_time = 15 if self._reconnect_failures > 10 else 1
                        if self._stop_consuming_event.wait(sleep_time):
                            break
        except (KeyboardInterrupt, SystemExit):
            LOGGER.debug('AmqpConnection monitoring_thread exiting due to process exit')

    def _consumer_thread_func(self):  # pylint: disable=too-many-branches
        """
        The thread function for the consumer thread.

        It will ask Pika to process any messages it obtains. Pika processes
        messages by invoking the specified callback function which in our
        case is ``_on_message`` found in
        :class:`systemlink.messagebus.amqp_channel.AmqpChannel`.
        """
        try:
            LOGGER.debug('AmqpConnection consume!')
            if self._heartbeat_only:
                process_time = 0
                sleep_time = 1
            else:
                process_time = 1
                sleep_time = 0.0001
            while not self._consumer_thread_should_stop:
                if not self._connected:
                    if self._auto_reconnect:
                        # Sleep a second waiting for the reconnect.
                        if self._stop_consuming_event.wait(1):
                            break
                        continue
                    else:
                        # We are disconnected and there is no auto-reconnect.
                        # Time to exit this thread.
                        break

                with self._connection_lock:
                    if self._consumer_thread_should_stop:
                        break
                    try:
                        if not self._connection:
                            raise_connection_closed()
                        with self._convert_error_contextmanager(
                                default_error_name='Skyline.AMQPErrorPerformingBasicConsume'):
                            for amqp_channel in self._amqp_channels.values():
                                amqp_channel.consume(self._auto_ack)
                            self._connection.process_data_events(process_time)
                    except Exception as exc:  # pylint: disable=broad-except
                        exc_name = exc.__class__.__name__
                        LOGGER.error(
                            'Error when consuming. %s: %s',
                            exc_name, exc, exc_info=True
                        )
                if self._stop_consuming_event.wait(sleep_time):
                    break
        except (KeyboardInterrupt, SystemExit):
            LOGGER.debug('AmqpConnection consume exiting due to process exit')
        with self._connection_lock:
            for amqp_channel in self._amqp_channels.values():
                if amqp_channel.channel:
                    amqp_channel.cancel_consume()
