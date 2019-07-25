# systemlink-test-result-subscriber-example-service
SystemLink service example for subscribing to test result notifications

SystemLink allows launching python projects as SystemLink services.  The SystemLink service manager detects new service descriptors which instruct the service manager which executables to launch.  The service manager is capable of launching C# DLLs which implement the ManagedServiceBase class, but can also launch external executable applications which implement the ManagedServiceBase as well.  In this case, the ManagedServiceBase is provided by the SystemLink python SDK, and provides the control messages and configuration through the Service Manager.

# 1.  Initial Setup
Copy the files in the two base folders (ProgramData and Program Files) to your SystemLink server.

# 2.  Restart the SystemLink Service Manager
Using the SystemLink Server Configuration application, click restart to re-launch the application.  The service descriptors are read only once when the service starts, so the Service Manager must be restarted to detect newly installed services.

# 3.  Customize the Test Result Subscriber example service
The Test Result Subscriber is a basic example that can be modified to perform tasks when a test result notification message is received.  The example implementation shows how the service subscribes to specific messages and defines callbacks to run when those events occur.

Modify the ```/Program Files/Skyline/TestResultSubscriberExample/systemlink/testresultsubscriberexampleservice/handlers/amqp_handlers.py``` file's ```test_result_broadcast``` method to insert your custom code.

    def test_result_broadcast(
            self,
            generic_message: GenericMessage,
        ):
        """
        :param generic_message: An object representing the AMQP message.
        """
        # Log that the broadcast was received.
        # This is logged at ERROR level so that it will appear in the log.
        # Logging level should be decreased or removed once implementation and debugging is completed.
        # Optionally, logging could be done to a tracepoint instead.
        LOGGER.error('received test result broadcast!')
        # TODO: Customize the code here to perform your task
