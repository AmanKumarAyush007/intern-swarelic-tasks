# Exercise 4.3 — Agent Flow Simulation

## 🎯 Objective

Build a **state machine** that simulates an agent's call handling lifecycle. This teaches you how Swarelic models agent availability and call states.

**Time estimate:** 4–5 hours

---

## Background

In Swarelic, every agent goes through a defined set of states:

```
OFFLINE → ONLINE → AVAILABLE → RINGING → ON_CALL → WRAPPING_UP → AVAILABLE
                              ↑                                        │
                              └────────────────────────────────────────┘
```

State transitions are triggered by events:
- `login` — Agent logs into the system
- `ready` — Agent marks themselves available
- `call_received` — System assigns a call
- `call_accepted` — Agent picks up
- `call_ended` — Call disconnects
- `wrap_up_complete` — Agent finishes post-call notes
- `logout` — Agent logs out

Invalid transitions (e.g., going from OFFLINE to ON_CALL) must be rejected with a clear error.

---

## 📋 Requirements

### 1. State Machine (`agent_flow/state_machine.py`)

```python
from enum import Enum, auto
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable

class AgentState(Enum):
    OFFLINE       = auto()
    ONLINE        = auto()
    AVAILABLE     = auto()
    RINGING       = auto()
    ON_CALL       = auto()
    WRAPPING_UP   = auto()
    BREAK         = auto()

class AgentEvent(Enum):
    LOGIN           = auto()
    READY           = auto()
    CALL_RECEIVED   = auto()
    CALL_ACCEPTED   = auto()
    CALL_REJECTED   = auto()  # Agent rejects call → back to AVAILABLE
    CALL_ENDED      = auto()
    WRAP_UP_DONE    = auto()
    TAKE_BREAK      = auto()  # From AVAILABLE → BREAK
    END_BREAK       = auto()  # From BREAK → AVAILABLE
    LOGOUT          = auto()

@dataclass
class StateTransition:
    from_state: AgentState
    event: AgentEvent
    to_state: AgentState
    guard: Callable | None = None      # Optional condition that must be True
    on_enter: Callable | None = None   # Side effect when entering new state

class AgentStateMachine:
    TRANSITIONS: list[StateTransition] = [
        # TODO: Define all valid transitions here
        # Example:
        # StateTransition(AgentState.OFFLINE, AgentEvent.LOGIN, AgentState.ONLINE),
    ]

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.state = AgentState.OFFLINE
        self.history: list[dict] = []
        self._current_call_id: str | None = None

    def trigger(self, event: AgentEvent, **kwargs) -> AgentState:
        """
        Apply an event to the current state.
        Returns the new state on success.
        Raises InvalidTransitionError if no valid transition exists.
        """
        # TODO: Implement this
        pass

    def can_trigger(self, event: AgentEvent) -> bool:
        """Return True if the event is valid in the current state."""
        # TODO: Implement this
        pass

    def get_history(self) -> list[dict]:
        """Return chronological list of state transitions."""
        return self.history


class InvalidTransitionError(Exception):
    """Raised when an event cannot be applied in the current state."""
    pass
```

### 2. Event Log (`agent_flow/event_log.py`)

Each transition should be recorded:

```python
{
    "timestamp": "2024-01-15T14:30:00",
    "agent_id": "alice",
    "from_state": "AVAILABLE",
    "event": "CALL_RECEIVED",
    "to_state": "RINGING",
    "metadata": {"call_id": "call-abc123"}
}
```

### 3. Agent Session (`agent_flow/session.py`)

Track metrics for a complete agent session:

```python
class AgentSession:
    def __init__(self, agent_id: str):
        self.machine = AgentStateMachine(agent_id)
        self.session_start = datetime.now()
        self._calls_handled = 0
        self._total_call_time_secs = 0
        self._total_wrap_time_secs = 0

    def process_event(self, event: AgentEvent, **kwargs) -> dict:
        """Process an event and return a status dict."""
        # TODO: delegate to state machine + record timing metrics
        pass

    def get_metrics(self) -> dict:
        """
        Return session metrics:
        - session_duration_secs
        - calls_handled
        - avg_call_duration_secs
        - availability_pct  (time in AVAILABLE / total online time)
        - current_state
        """
        # TODO: Implement this
        pass
```

### 4. Unit Tests (`agent_flow/tests/test_state_machine.py`)

Write at minimum **12 test cases**:

```python
class TestValidTransitions:
    def test_login_from_offline(self): ...
    def test_ready_from_online(self): ...
    def test_call_received_from_available(self): ...
    def test_call_accepted_from_ringing(self): ...
    def test_call_ended_from_on_call(self): ...
    def test_wrap_up_done_from_wrapping_up(self): ...
    def test_full_happy_path(self): ...  # offline → ... → available (one full cycle)

class TestInvalidTransitions:
    def test_cannot_accept_call_from_offline(self): ...
    def test_cannot_go_on_call_directly(self): ...
    def test_invalid_raises_exception(self): ...

class TestMetrics:
    def test_calls_handled_increments(self): ...
    def test_session_metrics_structure(self): ...
```

---

## ✅ Acceptance Criteria

- [ ] All defined transitions in `TRANSITIONS` list match the state diagram
- [ ] `InvalidTransitionError` raised for invalid events
- [ ] `trigger()` records entry in `history` list
- [ ] `can_trigger()` returns False for invalid transitions without raising
- [ ] Full happy-path cycle works: OFFLINE → ON_CALL → AVAILABLE
- [ ] `get_metrics()` returns all required keys
- [ ] All 12+ tests pass: `pytest agent_flow/tests/ -v`

---

## 💡 Hints

- The `TRANSITIONS` list is essentially a lookup table — find the matching row
- Use `datetime.now()` for timing, and track state entry times
- `CALL_REJECTED` is important: what state should the agent go back to?
- `BREAK` state: agents can only take a break from `AVAILABLE`

---

## 📚 References

- [State Machine Pattern](https://refactoring.guru/design-patterns/state)
- Python `enum` module
- Python `datetime` module
