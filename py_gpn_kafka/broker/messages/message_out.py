from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class MessageOut:
    """A frozen dataclass representing an outgoing message.

    Attributes:
        value: The main content of the message as bytes, or None if no payload.
        key: An optional key associated with the message as bytes, used for routing. None if no key is provided.
        headers: Optional list of header tuples where each tuple consists of a string
            header name and bytes header value. None if no headers are provided.
    """

    value: Optional[bytes]
    key: Optional[bytes]
    headers: Optional[list[tuple[str, bytes]]]
