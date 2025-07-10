from abc import ABC, abstractmethod
from typing import Any


class BasePresenter(ABC):
    """Abstract base class for all presenters.

    Presenters are responsible for converting response data into a specific output format.
    """

    @abstractmethod
    def present(self, response: Any) -> Any:
        """Transforms the response data into the desired output format.

        Args:
            response: The input data to be presented.

        Returns:
            The transformed data in the desired output format.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """

        ...
