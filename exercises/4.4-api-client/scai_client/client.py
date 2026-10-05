"""
scai_client/client.py — Starter for Exercise 4.4

TODO: Implement _request() and all the call log methods.
"""
import requests
from .config import SCAIClientConfig
from .auth import TokenManager
from .exceptions import SCAIAPIError, SCAIAuthError, SCAINotFoundError, SCAIValidationError


class SCAIClient:
    """
    Python client for the Swarelic SCAI REST API.

    Usage:
        config = SCAIClientConfig(
            base_url='http://localhost:8000',
            username='alice',
            password='secret'
        )
        client = SCAIClient(config)
        logs = client.list_call_logs(status='completed')
    """

    def __init__(self, config: SCAIClientConfig):
        self._config = config
        self._token_manager = TokenManager(
            base_url=config.base_url,
            username=config.username,
            password=config.password,
            timeout=config.timeout,
        )
        self._session = requests.Session()
        self._session.verify = config.verify_ssl

    def _request(self, method: str, path: str, **kwargs) -> dict | None:
        """
        Make an authenticated HTTP request to the SCAI API.

        Handles:
        - Automatic Authorization header injection
        - Token refresh on 401 (retry once)
        - 404 → SCAINotFoundError
        - 400 → SCAIValidationError
        - Other 4xx/5xx → SCAIAPIError

        Args:
            method: HTTP method ('GET', 'POST', 'PATCH', 'DELETE')
            path: API path, e.g. '/api/v1/call-logs/'
            **kwargs: passed to requests.Session.request()

        Returns:
            Parsed JSON dict, or None for 204 No Content.
        """
        # TODO: Implement this
        raise NotImplementedError("_request() not implemented")

    # ── Call Logs ────────────────────────────────────────────────

    def list_call_logs(self, status: str = None, page: int = 1,
                       page_size: int = 20, search: str = None) -> dict:
        """
        GET /api/v1/call-logs/
        Returns paginated response: {count, next, previous, results}
        """
        # TODO: build params dict and call _request
        raise NotImplementedError("list_call_logs() not implemented")

    def get_call_log(self, call_id: int) -> dict:
        """GET /api/v1/call-logs/{id}/"""
        raise NotImplementedError("get_call_log() not implemented")

    def create_call_log(self, agent_name: str, caller_number: str,
                        duration_secs: int, status: str, notes: str = '') -> dict:
        """POST /api/v1/call-logs/ — Returns the created call log dict."""
        raise NotImplementedError("create_call_log() not implemented")

    def update_call_log(self, call_id: int, **fields) -> dict:
        """PATCH /api/v1/call-logs/{id}/ — Partial update."""
        raise NotImplementedError("update_call_log() not implemented")

    def delete_call_log(self, call_id: int) -> None:
        """DELETE /api/v1/call-logs/{id}/ — Returns None on success."""
        raise NotImplementedError("delete_call_log() not implemented")
