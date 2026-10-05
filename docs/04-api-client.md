# Exercise 4.4 — API Client for SCAI

## 🎯 Objective

Build a production-quality Python **API client library** for the Swarelic SCAI REST API. This is how internal tools, scripts, and integrations talk to the platform.

**Time estimate:** 4–5 hours

---

## Background

The Swarelic platform exposes a REST API at `/api/v1/`. Internal tooling (dashboards, CLI tools, integrations) needs a clean, reusable Python client — not raw `requests` calls scattered everywhere.

This exercise teaches you **client library design patterns**: authentication management, error handling, type safety, and testability.

---

## 📋 Requirements

### 1. Client Configuration (`scai_client/config.py`)

```python
from dataclasses import dataclass

@dataclass
class SCAIClientConfig:
    base_url: str         # e.g. "http://localhost:8000"
    username: str
    password: str
    timeout: int = 30
    max_retries: int = 3
    verify_ssl: bool = True

    def __post_init__(self):
        # Validate: base_url must start with http:// or https://
        # Validate: timeout must be > 0
        # Validate: username and password must be non-empty strings
        pass
```

### 2. Authentication Manager (`scai_client/auth.py`)

```python
import requests
from datetime import datetime, timedelta

class TokenManager:
    def __init__(self, base_url: str, username: str, password: str, timeout: int):
        self._base_url = base_url
        self._username = username
        self._password = password
        self._timeout = timeout
        self._access_token: str | None = None
        self._refresh_token: str | None = None
        self._expires_at: datetime | None = None

    def get_access_token(self) -> str:
        """
        Return a valid access token.
        Auto-refreshes if token is within 60 seconds of expiry.
        Auto-logs in if no token exists.
        """
        # TODO: Implement this
        pass

    def _login(self) -> None:
        """POST /api/auth/token/ and store tokens."""
        # TODO: Implement this
        pass

    def _refresh(self) -> None:
        """POST /api/auth/token/refresh/ with refresh token."""
        # TODO: Implement this
        # Fall back to _login() if refresh fails
        pass

    def invalidate(self) -> None:
        """Clear stored tokens (e.g. on logout or 401 error)."""
        self._access_token = None
        self._refresh_token = None
        self._expires_at = None
```

### 3. Base Client (`scai_client/client.py`)

```python
import requests
from .config import SCAIClientConfig
from .auth import TokenManager
from .exceptions import SCAIAPIError, SCAIAuthError, SCAINotFoundError

class SCAIClient:
    def __init__(self, config: SCAIClientConfig):
        self._config = config
        self._token_manager = TokenManager(
            config.base_url, config.username, config.password, config.timeout
        )
        self._session = requests.Session()

    def _request(self, method: str, path: str, **kwargs) -> dict:
        """
        Make an authenticated API request.
        - Automatically adds Authorization header
        - On 401: refreshes token and retries ONCE
        - On 404: raises SCAINotFoundError
        - On 4xx: raises SCAIAPIError with the error message from response body
        - On 5xx: raises SCAIAPIError
        - Returns parsed JSON dict on success
        """
        # TODO: Implement this
        pass

    # ── Call Logs ───────────────────────────────────────────────
    def list_call_logs(self, status: str = None, page: int = 1, page_size: int = 20) -> dict:
        """GET /api/v1/call-logs/ — Returns paginated response dict."""
        params = {'page': page, 'page_size': page_size}
        if status:
            params['status'] = status
        return self._request('GET', '/api/v1/call-logs/', params=params)

    def get_call_log(self, call_id: int) -> dict:
        """GET /api/v1/call-logs/{id}/"""
        return self._request('GET', f'/api/v1/call-logs/{call_id}/')

    def create_call_log(self, agent_name: str, caller_number: str,
                         duration_secs: int, status: str, notes: str = '') -> dict:
        """POST /api/v1/call-logs/"""
        return self._request('POST', '/api/v1/call-logs/', json={
            'agent_name': agent_name,
            'caller_number': caller_number,
            'duration_secs': duration_secs,
            'status': status,
            'notes': notes,
        })

    def update_call_log(self, call_id: int, **fields) -> dict:
        """PATCH /api/v1/call-logs/{id}/"""
        return self._request('PATCH', f'/api/v1/call-logs/{call_id}/', json=fields)

    def delete_call_log(self, call_id: int) -> None:
        """DELETE /api/v1/call-logs/{id}/"""
        self._request('DELETE', f'/api/v1/call-logs/{call_id}/')
```

### 4. Custom Exceptions (`scai_client/exceptions.py`)

```python
class SCAIAPIError(Exception):
    """Base exception for all SCAI API errors."""
    def __init__(self, message: str, status_code: int = None, response_body: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body

class SCAIAuthError(SCAIAPIError):
    """Raised on 401/403 responses."""
    pass

class SCAINotFoundError(SCAIAPIError):
    """Raised on 404 responses."""
    pass

class SCAIValidationError(SCAIAPIError):
    """Raised on 400 responses with validation errors."""
    def __init__(self, message: str, errors: dict):
        super().__init__(message, 400, errors)
        self.errors = errors
```

### 5. Unit Tests with Mocking (`scai_client/tests/test_client.py`)

Use `unittest.mock` or `responses` library to mock HTTP calls:

```python
import pytest
import responses  # pip install responses
from scai_client.client import SCAIClient
from scai_client.config import SCAIClientConfig
from scai_client.exceptions import SCAINotFoundError, SCAIValidationError

@pytest.fixture
def client():
    config = SCAIClientConfig(
        base_url='http://test.local',
        username='test',
        password='testpass'
    )
    return SCAIClient(config)

class TestAuthentication:
    @responses.activate
    def test_auto_login_on_first_request(self, client): ...
    def test_token_refresh_before_expiry(self, client): ...
    def test_fallback_to_login_on_refresh_failure(self, client): ...

class TestCallLogs:
    @responses.activate
    def test_list_call_logs_returns_paginated(self, client): ...
    @responses.activate
    def test_get_call_log_not_found_raises(self, client): ...
    @responses.activate
    def test_create_call_log_returns_dict(self, client): ...
    @responses.activate
    def test_delete_call_log_returns_none(self, client): ...

class TestErrorHandling:
    @responses.activate
    def test_400_raises_validation_error(self, client): ...
    @responses.activate
    def test_500_raises_api_error(self, client): ...
    @responses.activate
    def test_401_triggers_token_refresh(self, client): ...
```

---

## ✅ Acceptance Criteria

- [ ] `SCAIClientConfig` raises `ValueError` on invalid inputs
- [ ] `TokenManager.get_access_token()` auto-logs in on first call
- [ ] Token refresh is triggered when < 60s from expiry
- [ ] `SCAINotFoundError` raised on 404
- [ ] `SCAIValidationError` raised on 400 with `errors` dict
- [ ] All CRUD methods for call logs work correctly
- [ ] All 10+ tests pass with mocked HTTP responses
- [ ] Client is usable as: `from scai_client import SCAIClient, SCAIClientConfig`

---

## 💡 Hints

- Store token expiry as `datetime.now() + timedelta(seconds=<lifetime>)`
- Use a `responses` decorator to intercept HTTP calls in tests — never hit real network in tests
- Make `_request()` a single place that handles all HTTP logic — don't repeat it in each method
- The `**kwargs` pattern on `_request` lets you pass `json=`, `params=`, `data=` freely

---

## 📚 References

- [responses library](https://github.com/getsentry/responses)
- [requests.Session docs](https://requests.readthedocs.io/en/latest/user/advanced/)
- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
