import json

from pydantic import BaseModel

from py_gpn_kafka.broker.presenters import BasePresenter


class ResponseJsonBytesPresenter(BasePresenter):
    """Presenter that converts Pydantic models to JSON-encoded bytes.

    This presenter takes a Pydantic BaseModel as input and returns it as
    a JSON string encoded into bytes.
    """

    def present(self, response: BaseModel) -> bytes:
        """Converts a Pydantic model to JSON-encoded bytes.

        Args:
            response: A Pydantic BaseModel instance to be converted.

        Returns:
            The JSON representation of the model encoded as bytes.
        """
        return json.dumps(response.dict(), separators=(",", ":")).encode()
