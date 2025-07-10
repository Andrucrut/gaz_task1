# вот эта функция в последствии должна будет ипортироваться из модуля с настройками

import os
from typing import Any


def get_env_var(key: str, default: Any = None) -> Any:
    """Retrieves and validates an environment variable.

    Args:
        key (str): The name of the environment variable to retrieve.
        default (Any): The default value for the environment variable.

    Returns:
        The value of the environment variable, stripped of leading/trailing whitespace.

    Raises:
        Exception: If the environment variable is not found or contains only whitespace.
    """
    try:
        variable = os.environ[key].strip()
        if not variable:
            if default:
                return default
            raise Exception(f"{key} variable found, but empty")
        return variable
    except KeyError:
        if default:
            return default
        raise Exception(f"{key} variable not found")
