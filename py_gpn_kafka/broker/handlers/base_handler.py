from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel, ValidationError

from py_gpn_kafka.broker.messages import MessageIn, MessageOut
from py_gpn_kafka.broker.presenters import BasePresenter
from py_gpn_kafka.broker.producer import Producer
from py_gpn_kafka.common.logger import logger
from py_gpn_kafka.models.deserializers import TaskId
from py_gpn_kafka.models.errors import BaseError

OutputT = TypeVar("OutputT", bound=BaseModel)


class BaseHandler(Generic[OutputT], ABC):
    """Abstract base class for message handlers.

    Provides common functionality for processing messages including validation,
    execution, error handling, and response production.

    Attributes:
        producer: Producer instance for sending output messages.
        presenter: Presenter instance for formatting output messages.
    """

    producer: Producer = None
    presenter: BasePresenter = None

    def init_base(self, producer: Producer, presenter: BasePresenter) -> None:
        """Initializes the base handler with required dependencies.

        Args:
            producer: Kafka message producer instance.
            presenter: Message presentation/formatter instance.
        """
        self.producer = producer
        self.presenter = presenter

    async def handle(self, message_in: MessageIn) -> MessageOut:
        """Processes an incoming message and produces an appropriate response.

        The method handles the complete message lifecycle:
        1. Initializes a default error response
        2. Attempts to validate and process the message
        3. Catches and handles any exceptions
        4. Produces an output message with appropriate status headers
        5. Returns the output message

        Args:
            message_in: The incoming message to process.

        Returns:
            The response message with status headers.
        """
        response = BaseError()
        value = self.presenter.present(response)
        headers = [("status", b"error")]
        try:
            key = TaskId.model_validate_json(message_in.key)
            response = await self.execute(message_in)
            logger.info(f"Response has been received for message with key={message_in.key.decode('utf-8')!r}")
            value = self.presenter.present(response)
            headers = [("status", b"success")]
        except (Exception, ValidationError) as e:
            print(e)
            response.type = type(e).__name__
            response.message = str(e)
            value = self.presenter.present(response)
            logger.error(
                f"Failed handle message with key={message_in.key.decode('utf-8')!r} and value={message_in.value.decode('utf-8')!r} due {type(e).__name__} with error message: {str(e)}"
            )
        finally:
            message_out = MessageOut(
                key=message_in.key,
                value=value,
                headers=headers,
            )
            await self.producer.produce_message(message_out)
            return message_out

    @abstractmethod
    async def process_business_logic(self, input_bytes: bytes) -> OutputT:
        """Abstract method containing business logic for message processing.

        Args:
            input_bytes: Raw bytes from the incoming message to process.

        Returns:
            Processed output as a Pydantic model.
        """
        ...

    async def execute(self, message_in: MessageIn) -> OutputT:
        """Execute the message processing pipeline.

        Args:
            message_in: The incoming message to process.

        Returns:
            The response object to be presented and sent as output.

        Raises:
            Exception: Any exception that occurs during processing will be caught
                and handled by the `handle` method.
        """
        logger.info(f"Starting processing for message with key={message_in.key.decode('utf-8')!r}")
        return await self.process_business_logic(message_in.value)
