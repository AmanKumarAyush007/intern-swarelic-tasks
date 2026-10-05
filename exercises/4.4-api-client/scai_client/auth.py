"""
scai_client/auth.py — Starter for Exercise 4.4

TODO: Implement TokenManager.get_access_token(), _login(), _refresh()
"""
import requests
from datetime import datetime, timedelta
from .exceptions import SCAIAuthError


class TokenManager:
    """Manages JWT access and refresh tokens for the SCAI API."""

    # Refresh token if less than this many seconds remain
    REFRESH_THRESHOLD_SECS = 60

    def __init__(self, base_url: str, username: str, password: str, timeout: int):
        self._base_url = base_url.rstrip('/')
        self._username = username
        self._password = password
        self._timeout = timeout
        self._access_token: str | None = None
        self._refresh_token: str | None = None
        self._expires_at: datetime | None = None

    def get_access_token(self) -> str:
        """
        Return a valid access token.
        - If no token: call _login()
        - If token expires within REFRESH_THRESHOLD_SECS: call _refresh()
        - Otherwise: return cached token

        Raises:
            SCAIAuthError: if login or refresh fails
        """
        # TODO: Implement this
        raise NotImplementedError("get_access_token() not implemented")

    def _login(self) -> None:
        """
        POST /api/auth/token/ with username+password.
        Store access_token, refresh_token, and compute expires_at.

        Raises:
            SCAIAuthError: on 401 or network error
        """
        # TODO: Implement this
        raise NotImplementedError("_login() not implemented")

    def _refresh(self) -> None:
        """
        POST /api/auth/token/refresh/ with the current refresh token.
        If refresh fails (e.g. refresh token expired), fall back to _login().

        Raises:
            SCAIAuthError: if both refresh AND login fail
        """
        # TODO: Implement this
        raise NotImplementedError("_refresh() not implemented")

    def invalidate(self) -> None:
        """Clear all stored token state."""
        self._access_token = None
        self._refresh_token = None
        self._expires_at = None

    @property
    def is_expired(self) -> bool:
        """True if the access token has expired or is within threshold."""
        if self._expires_at is None:
            return True
        remaining = (self._expires_at - datetime.now()).total_seconds()
        return remaining < self.REFRESH_THRESHOLD_SECS
