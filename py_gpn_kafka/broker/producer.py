from aiokafka import AIOKafkaProducer

from py_gpn_kafka.broker.messages import MessageOut
from py_gpn_kafka.common.logger import logger


class Producer:
    """A Kafka message producer for sending messages to a specified topic.

    Attributes:
        _connection_url (str): The URL for connecting to the Kafka broker.
        _topic (str): The topic to which messages will be produced.
    """

    def __init__(self, connection_url: str, topic: str) -> None:
        """Initializes the Producer with connection details and topic.

        Args:
            connection_url: The URL of the Kafka broker to connect to.
            topic: The name of the Kafka topic to produce messages to.
        """
        self._connection_url = connection_url
        self._topic = topic

    async def produce_message(self, message: MessageOut) -> None:
        """Produces a message to the configured Kafka topic.

        Creates a producer instance, starts it, sends the message, and ensures proper
        cleanup. Handles exceptions during message production.

        Args:
            message: The message to be sent, containing key, value, and headers.

        Raises:
            Exception: Re-raises any exception that occurs during producer startup.
        """
        broker_producer = self.__build_broker_producer()
        await self.__start_broker_producer(broker_producer)
        try:
            await broker_producer.send(
                topic=self._topic,
                key=message.key,
                value=message.value,
                headers=message.headers,
            )
            await broker_producer.flush()
        except Exception as e:
            logger.error(f"Failed to produce message with {self._topic} - {message.key} due {e}")
        finally:
            await broker_producer.stop()

    async def __start_broker_producer(self, broker_producer: AIOKafkaProducer) -> None:
        """Starts the Kafka producer instance.

        Args:
            broker_producer: The AIOKafkaProducer instance to start.

        Raises:
            Exception: If the producer fails to start, logs the error and re-raises.
        """
        try:
            await broker_producer.start()
        except Exception as e:
            logger.error(f"Failed to start consumer due to {e}")
            raise e

    def __build_broker_producer(self) -> AIOKafkaProducer:
        """Creates a new AIOKafkaProducer instance.

        Returns:
            A new producer instance configured with the connection URL.
        """
        return AIOKafkaProducer(bootstrap_servers=self._connection_url)
