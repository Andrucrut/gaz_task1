from typing import Optional

from py_gpn_kafka.broker.consumer import WorkflowConsumer
from py_gpn_kafka.broker.handlers import BaseHandler
from py_gpn_kafka.broker.presenters import BasePresenter, ResponseJsonBytesPresenter
from py_gpn_kafka.broker.producer import Producer
from py_gpn_kafka.core.config import BrokerConfig


def build_topic(prefix: str, name: str, suffix: Optional[str] = None) -> str:
    """Constructs a Kafka topic name from components.

    Args:
        prefix: The prefix for the topic.
        name: The main name for the topic.
        suffix: Optional suffix to append to the topic name.

    Returns:
        The constructed topic name.
    """
    if not suffix:
        return f"{prefix}_{name}"
    return f"{prefix}_{name}_{suffix}"


class ApiStructure:
    """A class for creating Kafka-related components with consistent configuration.

    This class provides methods to create topics, producers, handlers, and consumers
    using a shared BrokerConfig.

    Attributes:
        broker_config: The configuration object containing Kafka connection details
            and naming conventions.
    """

    def __init__(self, broker_config: BrokerConfig) -> None:
        """Initializes the ApiStructure with the given broker configuration.

        Args:
            broker_config: The configuration object for Kafka broker settings.
        """
        self.broker_config = broker_config

    def create_topic(self, topic_name: str, is_response: bool = False) -> str:
        """Creates a properly formatted topic name using the broker configuration.

        Args:
            topic_name: The base name for the topic.
            is_response: Whether this is a response topic (will use response suffix from config if True).

        Returns:
            The fully formatted topic name.
        """
        return build_topic(
            self.broker_config.TOPIC_PREFIX,
            topic_name,
            self.broker_config.RESPONSE_TOPIC_SUFFIX if is_response else None,
        )

    def create_producer(self, response_topic: str) -> Producer:
        """Creates a Kafka producer instance.

        Args:
            response_topic: The topic name this producer should publish to.

        Returns:
            A configured Producer instance.
        """
        return Producer(
            connection_url=self.broker_config.KAFKA_URL,
            topic=response_topic,
        )

    def create_handler(
        self,
        handler_cls: type(BaseHandler),
        producer: Producer,
        presenter: type(BasePresenter) = ResponseJsonBytesPresenter,
        *args,
        **kwargs,
    ) -> BaseHandler:
        """Creates a message handler instance.

        Args:
            handler_cls: The handler class to instantiate.
            producer: The producer instance the handler should use.
            presenter: The presenter class to use for formatting responses.
                Defaults to ResponseJsonBytesPresenter.
            *args: Additional positional arguments to pass to the handler
                constructor.
            **kwargs: Additional keyword arguments to pass to the handler
                constructor.

        Returns:
            An initialized handler instance.
        """

        handler = handler_cls(*args, **kwargs)
        handler.init_base(producer=producer, presenter=presenter())
        return handler

    def create_consumer(self, handler: BaseHandler) -> WorkflowConsumer:
        """Creates a Kafka consumer instance.

        Args:
            handler: The handler instance that will process consumed messages.

        Returns:
            A configured WorkflowConsumer instance.
        """
        return WorkflowConsumer(
            connection_url=self.broker_config.KAFKA_URL,
            handler=handler,
        )
