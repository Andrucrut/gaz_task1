from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class MessageIn:
    """A frozen dataclass representing an incoming message.

    This class encapsulates the key components of a message received from a message broker,
    including the topic, value, and optional key. The class is immutable (frozen=True).

    Attributes:
        topic: The topic where the message was published.
        value: The content of the message. Defaults to an empty bytes dictionary (b"{}") if not provided.
        key: The key for routing. The default value is None.
    """

    topic: bytes
    value: Optional[bytes]
    key: Optional[bytes]

    @classmethod
    def from_record(cls, record) -> "MessageIn":
        topic = getattr(record, "topic", None)
        if topic is None:
            raise ValueError("Topic must be provided for each message")
        return cls(
            topic=topic,
            value=getattr(record, "value", b"{}"),
            key=getattr(record, "key", None),
        )
