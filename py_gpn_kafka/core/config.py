from dataclasses import dataclass, field

from py_gpn_kafka.broker.handlers import BaseHandler
from py_gpn_kafka.broker.presenters import BasePresenter, ResponseJsonBytesPresenter
from py_gpn_kafka.core.env_wrapper import get_env_var


@dataclass
class TopicInfo:
    topic_name: str
    handler_cls: type(BaseHandler)
    presenter: type(BasePresenter) = field(default=ResponseJsonBytesPresenter)
    handler_kwargs: dict = field(default_factory=dict)
    handler_args: tuple = field(default_factory=tuple)


class BrokerConfig:
    """Stores configuration settings for the message broker loaded from environment variables.

    Attributes:
        KAFKA_URL (str): URL of the Kafka broker server.
        TOPIC_PREFIX (str): Prefix used for constructing all topic names.
        RESPONSE_TOPIC_SUFFIX (str): Suffix appended to response topics.
        TOPICS_INFO (list[TopicInfo]): List of topics and info about them.
    """

    KAFKA_URL: str = get_env_var("KAFKA_URL")
    TOPIC_PREFIX: str = get_env_var("TOPIC_PREFIX")
    RESPONSE_TOPIC_SUFFIX: str = get_env_var("RESPONSE_TOPIC_SUFFIX")
    TOPICS_INFO: list[TopicInfo] = None

    def __init__(self, topics_info: list[TopicInfo]) -> None:
        self.TOPICS_INFO = topics_info
