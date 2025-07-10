import asyncio
from typing import NoReturn, Protocol

from aiokafka import AIOKafkaConsumer

from py_gpn_kafka.broker.messages import MessageIn, MessageOut
from py_gpn_kafka.common.logger import logger


class SupportsHandle(Protocol):
    """Protocol defining the interface for message handlers."""

    async def handle(self, message_in: MessageIn) -> MessageOut:
        """Process an incoming message and return a response.

        Args:
            message_in: The incoming message to process.

        Returns:
            The response message after processing.
        """
        ...


class WorkflowConsumer:
    """A Kafka consumer for workflow messages with pause/resume capability.

    Attributes:
        _name: The name of the consumer (includes topic when consuming).
        _connection_url: The URL for connecting to Kafka.
        _handler: The message handler implementing SupportsHandle protocol.
        _resume_event: Event to control pause/resume state.
        _idle_event: Event to track when consumer is idle.
    """

    def __init__(self, connection_url: str, handler: SupportsHandle) -> None:
        """Initializes the WorkflowConsumer.

        Args:
            connection_url: The Kafka broker connection URL.
            handler: An object implementing the SupportsHandle protocol.
        """
        self._name = "Consumer(unknown_topic)"
        self._connection_url = connection_url
        self._handler = handler
        self._resume_event = asyncio.Event()
        self._resume_event.set()
        self._idle_event = asyncio.Event()
        self._set_idle()

    async def consume(self, topic: str) -> None:
        """Starts consuming messages from the specified topic.

        Args:
            topic: The Kafka topic to consume messages from.

        Raises:
            Exception: If consumer fails to start or handle messages.
        """
        self._name = f"Consumer({topic})"
        consumer = await self._build_kafka_consumer(topic)
        await self._start_kafka_consumer(consumer)
        try:
            await self._handle_records(consumer)
        except Exception as e:
            logger.error(f"{self._name} - failed to start consumer due to {e}")
            raise e
        finally:
            await consumer.stop()

    async def _build_kafka_consumer(self, topic: str) -> AIOKafkaConsumer:
        """Builds and returns an AIOKafkaConsumer instance.

        Args:
            topic: The topic to subscribe to.

        Returns:
            An initialized AIOKafkaConsumer instance.

        Raises:
            Exception: If consumer fails to build.
        """
        try:
            logger.info(f"Trying to build {self._name}")
            consumer = AIOKafkaConsumer(
                topic, bootstrap_servers=self._connection_url, group_id=f"{topic}_consumer_group"
            )
            logger.info(f"Successfully built {self._name}")
            return consumer
        except Exception as e:
            logger.error(f"Failed to build {self._name} due to {e}")
            raise e

    async def _start_kafka_consumer(self, consumer: AIOKafkaConsumer) -> None:
        """Starts the Kafka consumer.

        Args:
            consumer: The AIOKafkaConsumer instance to start.

        Raises:
            Exception: If consumer fails to start.
        """
        try:
            logger.info(f"Starting {self._name}")
            await consumer.start()
            logger.info(f"Successfully started {self._name}")
        except Exception as e:
            logger.error(f"Failed to start {self._name} due to {e}")
            raise e

    async def _handle_records(self, consumer: AIOKafkaConsumer) -> NoReturn:
        """Continuously handles incoming records from the consumer.

        Args:
            consumer: The active AIOKafkaConsumer instance.

        Note:
            This method runs indefinitely until the consumer is stopped.
        """
        self._set_idle()
        if self._is_set_to_pause():
            await self._wait_to_resume()
        async for record in consumer:
            await self._wait_to_resume()
            self._set_active()
            message = MessageIn.from_record(record)
            logger.info(f"{self._name} - collect message {message.topic} - {message.key.decode('utf-8')!r}")
            await self._handler.handle(message)
            logger.info(f"{self._name} - processed message {message.topic} - {message.key.decode('utf-8')!r}")

            if self._is_set_to_pause():
                consumer.pause()
                self._set_idle()
                await self._wait_to_resume()
                consumer.resume()
            self._set_idle()

    def _set_idle(self) -> None:
        """Sets the consumer state to idle and logs the event."""
        self._idle_event.set()
        logger.info(f"{self._name} is idle now")

    def _set_active(self) -> None:
        """Sets the consumer state to active and logs the event."""
        self._idle_event.clear()
        logger.info(f"{self._name} is active now")

    def _is_set_to_pause(self) -> bool:
        """Checks if consumer is set to pause.

        Returns:
            True if consumer should pause, False otherwise.
        """
        return not self._resume_event.is_set()

    async def _wait_to_resume(self) -> None:
        """Waits for resume signal if consumer is paused."""
        logger.info(f"{self._name} wait for resume now")
        await self._resume_event.wait()
        if await self.is_idle():
            logger.info(f"{self._name} is idle now")

    async def pause(self) -> None:
        """Pauses message consumption after current message completes.

        Waits for consumer to become idle before returning.
        """
        self._resume_event.clear()
        await self._idle_event.wait()
        logger.info(f"{self._name} is paused now")

    async def resume(self) -> None:
        """Resumes message consumption."""
        self._resume_event.set()
        logger.info(f"{self._name} is resumed now")

    async def is_idle(self) -> bool:
        """Checks if consumer is currently idle.

        Returns:
            True if consumer is idle, False otherwise.
        """
        return self._idle_event.is_set()
