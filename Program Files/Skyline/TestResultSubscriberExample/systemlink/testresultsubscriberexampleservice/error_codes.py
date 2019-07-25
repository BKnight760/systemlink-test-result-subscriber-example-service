# -*- coding: utf-8 -*-
"""
Registration of error codes to the Error Code Registry.
"""
from __future__ import absolute_import

# Import local libs
# pylint: disable=import-error
from systemlink.messagebus import error_code_registry
# pylint: enable=import-error

# This will register the following error codes:
#   Skyline.InternalServiceError [-251000]
#   Skyline.RequestTimedOut [-251001]
#   Skyline.IOError [-251002]
#   Skyline.OutOfMemory [-251003]
#   Skyline.Exception [-251004]
#   Skyline.FailedToParse [-251005]
#   Skyline.InvalidSemaphoreInitialization [-251006]
#   Skyline.InsufficientResources [-251007]
#   Skyline.NotSupported [-251008]
#   Skyline.InsufficientPrivileges [-251009]
#   Skyline.MultipleInitializations [-251010]
#   Skyline.NoSkylineConfigurations [-251011]
#   Skyline.ConfigDirectoryNotFound [-251012]
#   Skyline.DuplicateConfigurationId [-251013]
#   Skyline.EndOfStream [-251014]
#   Skyline.QueueEmpty [-251015]
#   Skyline.FailedToInitializeNISSL [-251016]
#   Skyline.AMQPErrorOpeningTCPConnection [-251017]
#   Skyline.AMQPErrorClosingTCPConnection [-251018]
#   Skyline.AMQPErrorEndingTCPConnection [-251019]
#   Skyline.AMQPErrorCreatingTCPSocket [-251020]
#   Skyline.AMQPErrorCreatingSSLSocket [-251021]
#   Skyline.AMQPErrorOpeningSocket [-251022]
#   Skyline.AMQPErrorSettingCACertificate [-251023]
#   Skyline.AMQPErrorFailedToLogIn [-251024]
#   Skyline.AMQPErrorOpeningChannel [-251025]
#   Skyline.AMQPErrorDeclaringQueue [-251026]
#   Skyline.AMQPErrorObtainingQueueName [-251027]
#   Skyline.AMQPErrorBindingQueue [-251028]
#   Skyline.AMQPErrorUnbindingQueue [-251029]
#   Skyline.AMQPErrorDeclaringExchange [-251030]
#   Skyline.AMQPErrorPerformingBasicConsume [-251031]
#   Skyline.AMQPErrorPublishingMessage [-251032]
#   Skyline.AMQPErrorDequeueingMessage [-251033]
#   Skyline.AMQPErrorCertificateExpired [-251034]
#   Skyline.AMQPErrorPeerVerifyFailed [-251035]
#   Skyline.FailedToLoadCertificate [-251036]
#   Skyline.UnexpectedException [-251037]
#   Skyline.NotFound [-251038]
#   Skyline.UnableToLoadClientLibrary [-251039]
#   Skyline.AMQPErrorSettingQoS [-251040]
#   Skyline.OneOrMoreErrorsOccurred [-251041]
#   SkylineWebServices.MethodNotAllowed [-252200]
#   SkylineWebServices.SkipMustBePositive [-252201]
#   SkylineWebServices.TakeMustBePositive [-252202]
#   SkylineWebServices.MalformedProperty [-252203]
#   SkylineWebServices.MalformedJsonRequestBody [-252204]
#   SkylineWebServices.MissingRequiredJsonKey [-252205]
#   SkylineWebServices.InvalidJsonValueForKey [-252206]
#   SkylineWebServices.InvalidJsonDataTypeForKey [-252207]
#   SkylineWebServices.NoQueryParameterSpecified [-252208]
#   SkylineWebServices.UnknownQueryParameter [-252209]
#   SkylineWebServices.InvalidQueryParameter [-252210]
#   SkylineWebServices.MustSelectAFileForUpload [-252211]
#   SkylineWebServices.EmptyRequestBody [-252212]
#   SkylineWebServices.InvalidJsonDataTypeForElementInKey [-252213]
#   SkylineWebServices.InvalidJsonValueForElementInKey [-252214]
#   SkylineWebServices.NoElementsInJsonArray [-252215]
#   SkylineWebServices.ErrorParsingRequest [-252216]
#   SkylineWebServices.NotFound [-252217]
#   SkylineWebServices.InvalidValueForQueryParameter [-252218]
#   SkylineWebServices.MissingHandlerForUri [-252219]
#   SkylineWebServices.InvalidHandlerForUri [-252220]
#   SkylineWebServices.MissingRequiredUriParameter [-252221]
#   SkylineWebServices.UnexpectedMultipartBody [-252222]
#   SkylineWebServices.TimeoutReadingRequest [-252223]
#   SkylineWebServices.TimeoutSendingResponse [-252224]
#   SkylineWebServices.ErrorHandlingRequest [-252225]
#   SkylineWebServices.MalformedRequestEncoding [-252226]
#   SkylineWebServices.HttpStreamAborted [-252227]
#   SkylineWebServices.RequestDataTooLarge [-252228]
#   NotebookExecution.NotebookNotFound [-253700]
#   NotebookExecution.NotebookInsufficientPrivileges [-253701]
#   NotebookExecution.InvalidNotebook [-253702]
#   NotebookExecution.ExecutionNotFound [-253703]
#   NotebookExecution.CachedResultNotFound [-253704]

REGISTERED = False


def register_error_codes():  # pylint: disable=too-many-statements
    """
    Register error codes to the Error Code Registry.
    """
    # pylint: disable=line-too-long
    global REGISTERED  # pylint: disable=global-statement

    if REGISTERED:
        return

    # Right now we only support English.
    # Once we support more, use "locale.getdefaultlocale" to get the
    # system language.
    language = 'eng'

    if language == 'eng':
        error_code_registry.register(
            "Skyline",
            "InternalServiceError",
            "Internal Skyline service error.",
            -251000
        )
        error_code_registry.register(
            "Skyline",
            "RequestTimedOut",
            "Request timed out.",
            -251001
        )
        error_code_registry.register(
            "Skyline",
            "IOError",
            "I/O error.",
            -251002
        )
        error_code_registry.register(
            "Skyline",
            "OutOfMemory",
            "Out of memory.",
            -251003
        )
        error_code_registry.register(
            "Skyline",
            "Exception",
            "Skyline exception.",
            -251004
        )
        error_code_registry.register(
            "Skyline",
            "FailedToParse",
            "Failed to parse.",
            -251005
        )
        error_code_registry.register(
            "Skyline",
            "InvalidSemaphoreInitialization",
            "Invalid semaphore initialization.",
            -251006
        )
        error_code_registry.register(
            "Skyline",
            "InsufficientResources",
            "Insufficient resources.",
            -251007
        )
        error_code_registry.register(
            "Skyline",
            "NotSupported",
            "Not supported.",
            -251008
        )
        error_code_registry.register(
            "Skyline",
            "InsufficientPrivileges",
            "Insufficient privileges.",
            -251009
        )
        error_code_registry.register(
            "Skyline",
            "MultipleInitializations",
            "Attempt to reinitialize with multiple configurations.",
            -251010
        )
        error_code_registry.register(
            "Skyline",
            "NoSkylineConfigurations",
            "No Skyline configurations available.",
            -251011
        )
        error_code_registry.register(
            "Skyline",
            "ConfigDirectoryNotFound",
            "Skyline configurations directory not found.",
            -251012
        )
        error_code_registry.register(
            "Skyline",
            "DuplicateConfigurationId",
            "Duplicate configuration id.",
            -251013
        )
        error_code_registry.register(
            "Skyline",
            "EndOfStream",
            "End of stream.",
            -251014
        )
        error_code_registry.register(
            "Skyline",
            "QueueEmpty",
            "Queue empty.",
            -251015
        )
        error_code_registry.register(
            "Skyline",
            "FailedToInitializeNISSL",
            "Failed to initialize NI SSL.",
            -251016
        )
        error_code_registry.register(
            "Skyline",
            "AMQPErrorOpeningTCPConnection",
            "AMQP error: Failed to open TCP connection.",
            -251017
        )
        error_code_registry.register(
            "Skyline",
            "AMQPErrorClosingTCPConnection",
            "AMQP error: Failed to close TCP connection.",
            -251018
        )
        error_code_registry.register(
            "Skyline",
            "AMQPErrorEndingTCPConnection",
            "AMQP error: Failed to end TCP connection.",
            -251019
        )
        error_code_registry.register(
            "Skyline",
            "AMQPErrorCreatingTCPSocket",
            "AMQP error: Failed to create TCP socket.",
            -251020
        )
        error_code_registry.register(
            "Skyline",
            "AMQPErrorCreatingSSLSocket",
            "AMQP error: Failed to create SSL socket.",
            -251021
        )
        error_code_registry.register(
            "Skyline",
            "AMQPErrorOpeningSocket",
            "AMQP error: Failed to open socket.",
            -251022
        )
        error_code_registry.register(
            "Skyline",
            "AMQPErrorSettingCACertificate",
            "AMQP error: Failed to set CA certificate.",
            -251023
        )
        error_code_registry.register(
            "Skyline",
            "AMQPErrorFailedToLogIn",
            "AMQP error: Failed to log in.",
            -251024
        )
        error_code_registry.register(
            "Skyline",
            "AMQPErrorOpeningChannel",
            "AMQP error: Failed to open channel.",
            -251025
        )
        error_code_registry.register(
            "Skyline",
            "AMQPErrorDeclaringQueue",
            "AMQP error: Failed to declare queue.",
            -251026
        )
        error_code_registry.register(
            "Skyline",
            "AMQPErrorObtainingQueueName",
            "AMQP error: Failed to obtain queue name.",
            -251027
        )
        error_code_registry.register(
            "Skyline",
            "AMQPErrorBindingQueue",
            "AMQP error: Failed to bind queue.",
            -251028
        )
        error_code_registry.register(
            "Skyline",
            "AMQPErrorUnbindingQueue",
            "AMQP error: Failed to unbind queue.",
            -251029
        )
        error_code_registry.register(
            "Skyline",
            "AMQPErrorDeclaringExchange",
            "AMQP error: Failed to declare exchange.",
            -251030
        )
        error_code_registry.register(
            "Skyline",
            "AMQPErrorPerformingBasicConsume",
            "AMQP error: Failed to perform basic consume.",
            -251031
        )
        error_code_registry.register(
            "Skyline",
            "AMQPErrorPublishingMessage",
            "AMQP error: Failed to publish message.",
            -251032
        )
        error_code_registry.register(
            "Skyline",
            "AMQPErrorDequeueingMessage",
            "AMQP error: Failed to dequeue message.",
            -251033
        )
        error_code_registry.register(
            "Skyline",
            "AMQPErrorCertificateExpired",
            "AMQP error: Cetificate expired.",
            -251034
        )
        error_code_registry.register(
            "Skyline",
            "AMQPErrorPeerVerifyFailed",
            "AMQP error: Peer verify failed.",
            -251035
        )
        error_code_registry.register(
            "Skyline",
            "FailedToLoadCertificate",
            "Failed to load certificate.",
            -251036
        )
        error_code_registry.register(
            "Skyline",
            "UnexpectedException",
            "An unexpected exception occurred: {0}",
            -251037
        )
        error_code_registry.register(
            "Skyline",
            "NotFound",
            "Not found.",
            -251038
        )
        error_code_registry.register(
            "Skyline",
            "UnableToLoadClientLibrary",
            "Unable to load a client library. Ensure the NI SystemLink Client is installed.",
            -251039
        )
        error_code_registry.register(
            "Skyline",
            "AMQPErrorSettingQoS",
            "AMQP error: Failed to set quality of service.",
            -251040
        )
        error_code_registry.register(
            "Skyline",
            "OneOrMoreErrorsOccurred",
            "One or more errors occurred. See the contained list for details of each error.",
            -251041
        )
        error_code_registry.register(
            "SkylineWebServices",
            "MethodNotAllowed",
            "Method '{0}' not allowed.",
            -252200
        )
        error_code_registry.register(
            "SkylineWebServices",
            "SkipMustBePositive",
            "Skip must be a positive integer.",
            -252201
        )
        error_code_registry.register(
            "SkylineWebServices",
            "TakeMustBePositive",
            "Take must be a positive integer.",
            -252202
        )
        error_code_registry.register(
            "SkylineWebServices",
            "MalformedProperty",
            "Malformed property: '{0}'.",
            -252203
        )
        error_code_registry.register(
            "SkylineWebServices",
            "MalformedJsonRequestBody",
            "Malformed JSON request body.",
            -252204
        )
        error_code_registry.register(
            "SkylineWebServices",
            "MissingRequiredJsonKey",
            "Missing required JSON key: '{0}'.",
            -252205
        )
        error_code_registry.register(
            "SkylineWebServices",
            "InvalidJsonValueForKey",
            "Invalid JSON value for key '{0}'.",
            -252206
        )
        error_code_registry.register(
            "SkylineWebServices",
            "InvalidJsonDataTypeForKey",
            "Invalid JSON data type for for key '{0}'.",
            -252207
        )
        error_code_registry.register(
            "SkylineWebServices",
            "NoQueryParameterSpecified",
            "No query parameter specified.",
            -252208
        )
        error_code_registry.register(
            "SkylineWebServices",
            "UnknownQueryParameter",
            "Unknown query parameter: '{0}'.",
            -252209
        )
        error_code_registry.register(
            "SkylineWebServices",
            "InvalidQueryParameter",
            "Invalid '{0}' query parameter.",
            -252210
        )
        error_code_registry.register(
            "SkylineWebServices",
            "MustSelectAFileForUpload",
            "Must select a file for upload.",
            -252211
        )
        error_code_registry.register(
            "SkylineWebServices",
            "EmptyRequestBody",
            "Empty request body.",
            -252212
        )
        error_code_registry.register(
            "SkylineWebServices",
            "InvalidJsonDataTypeForElementInKey",
            "Invalid JSON data type for element in key '{0}'.",
            -252213
        )
        error_code_registry.register(
            "SkylineWebServices",
            "InvalidJsonValueForElementInKey",
            "Invalid JSON value for element in key '{0}'.",
            -252214
        )
        error_code_registry.register(
            "SkylineWebServices",
            "NoElementsInJsonArray",
            "At least one element must be provided in the JSON array '{0}'.",
            -252215
        )
        error_code_registry.register(
            "SkylineWebServices",
            "ErrorParsingRequest",
            "An error occurred while parsing the JSON request body: '{0}'.",
            -252216
        )
        error_code_registry.register(
            "SkylineWebServices",
            "NotFound",
            "The requested URI was not found.",
            -252217
        )
        error_code_registry.register(
            "SkylineWebServices",
            "InvalidValueForQueryParameter",
            "Invalid value for query parameter: '{0}'.",
            -252218
        )
        error_code_registry.register(
            "SkylineWebServices",
            "MissingHandlerForUri",
            "The handler for the requested URI is not available.",
            -252219
        )
        error_code_registry.register(
            "SkylineWebServices",
            "InvalidHandlerForUri",
            "The handler for the requested URI is invalid.",
            -252220
        )
        error_code_registry.register(
            "SkylineWebServices",
            "MissingRequiredUriParameter",
            "Missing required URI parameter: '{0}'.",
            -252221
        )
        error_code_registry.register(
            "SkylineWebServices",
            "UnexpectedMultipartBody",
            "Unexpected multipart/form-data request body.",
            -252222
        )
        error_code_registry.register(
            "SkylineWebServices",
            "TimeoutReadingRequest",
            "Time out reading request body.",
            -252223
        )
        error_code_registry.register(
            "SkylineWebServices",
            "TimeoutSendingResponse",
            "Time out writing response body.",
            -252224
        )
        error_code_registry.register(
            "SkylineWebServices",
            "ErrorHandlingRequest",
            "Error handling request.",
            -252225
        )
        error_code_registry.register(
            "SkylineWebServices",
            "MalformedRequestEncoding",
            "Malformed UTF-8 request body.",
            -252226
        )
        error_code_registry.register(
            "SkylineWebServices",
            "HttpStreamAborted",
            "HTTP stream was aborted.",
            -252227
        )
        error_code_registry.register(
            "SkylineWebServices",
            "RequestDataTooLarge",
            "HTTP request data is too large to buffer.",
            -252228
        )

    # pylint: enable=line-too-long
    REGISTERED = True
