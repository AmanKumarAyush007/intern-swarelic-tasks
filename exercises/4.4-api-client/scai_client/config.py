"""
scai_client/config.py — Starter for Exercise 4.4
"""
from dataclasses import dataclass


@dataclass
class SCAIClientConfig:
    base_url: str
    username: str
    password: str
    timeout: int = 30
    max_retries: int = 3
    verify_ssl: bool = True

    def __post_init__(self):
        """
        Validate configuration.

        Raises:
            ValueError: if base_url doesn't start with http:// or https://
            ValueError: if timeout <= 0
            ValueError: if username or password is empty
        """
        # TODO: Implement validation
        pass
