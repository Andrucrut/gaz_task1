import asyncio
from collections import defaultdict
from typing import NoReturn

from py_gpn_kafka.broker.structure import ApiStructure
from py_gpn_kafka.common.logger import logger
from py_gpn_kafka.core.config import BrokerConfig


class App:
    """A Kafka application that manages topic consumers and their lifecycle.

    The App class maintains a registry of consumers for different topics and
    provides methods to start all registered consumers.

    Attributes:
        _topic_to_consumers: A dictionary mapping topics to their registered consumers.
        _active_consumers: A list of currently active consumer tasks.
    """

    def __init__(self) -> None:
        """Initializes the App with empty consumer registries."""
        self._topic_to_consumers: dict[str, list] = defaultdict(list)
        self._active_consumers: list[asyncio.Task] = []

    def register_consumer(self, topic: str, consumer) -> None:
        """Registers a consumer for a specific topic.

        Args:
            topic: The topic name to register the consumer for.
            consumer: The consumer instance to register.
        """
        self._topic_to_consumers[topic].append(consumer)

    async def start(self) -> NoReturn:
        """Starts all registered consumers and runs them indefinitely.

        This method creates tasks for all registered consumers and runs them
        concurrently using asyncio.gather.
        """
        logger.info(f"kafka_app startup process has begun")
        for topic, consumers in self._topic_to_consumers.items():
            for consumer in consumers:
                consume_coro = consumer.consume(topic)
                self._active_consumers.append(asyncio.create_task(consume_coro))
        logger.info(f"kafka_app is now running")
        await asyncio.gather(*self._active_consumers)


def build_app(broker_config: BrokerConfig) -> App:
    """Builds and configures a Kafka application based on broker configuration.

    Creates an App instance and configures it with consumers, producers, and handlers
    for all topics specified in the broker configuration.

    Args:
        broker_config: Configuration object containing broker and topic information.

    Returns:
        A fully configured App instance ready to be started.
    """
    logger.info("Trying to build kafka_app")
    app = App()
    api_structure = ApiStructure(broker_config)
    for topic_info in broker_config.TOPICS_INFO:
        topic = topic_info.topic_name
        handler_cls = topic_info.handler_cls
        presenter = topic_info.presenter

        request_topic = api_structure.create_topic(topic)
        response_topic = api_structure.create_topic(topic, is_response=True)

        producer = api_structure.create_producer(response_topic)
        handler = api_structure.create_handler(
            handler_cls, producer, presenter, *topic_info.handler_args, **topic_info.handler_kwargs
        )
        consumer = api_structure.create_consumer(handler)
        app.register_consumer(
            topic=request_topic,
            consumer=consumer,
        )
    logger.info("Successfully built kafka_app")
    return app
