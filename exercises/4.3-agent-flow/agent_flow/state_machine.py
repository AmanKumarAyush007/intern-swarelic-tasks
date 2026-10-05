"""
agent_flow/state_machine.py — Starter for Exercise 4.3

TODO: Define all valid transitions in TRANSITIONS and implement
      trigger(), can_trigger() methods.

See docs/03-agent-flow.md for the full state diagram.
"""
from enum import Enum, auto
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Optional


class AgentState(Enum):
    OFFLINE     = auto()
    ONLINE      = auto()
    AVAILABLE   = auto()
    RINGING     = auto()
    ON_CALL     = auto()
    WRAPPING_UP = auto()
    BREAK       = auto()


class AgentEvent(Enum):
    LOGIN         = auto()
    READY         = auto()
    CALL_RECEIVED = auto()
    CALL_ACCEPTED = auto()
    CALL_REJECTED = auto()
    CALL_ENDED    = auto()
    WRAP_UP_DONE  = auto()
    TAKE_BREAK    = auto()
    END_BREAK     = auto()
    LOGOUT        = auto()


class InvalidTransitionError(Exception):
    """Raised when an event is not valid in the current state."""
    def __init__(self, state: AgentState, event: AgentEvent):
        self.state = state
        self.event = event
        super().__init__(
            f"Cannot trigger '{event.name}' from state '{state.name}'"
        )


@dataclass
class StateTransition:
    from_state: AgentState
    event: AgentEvent
    to_state: AgentState
    guard: Optional[Callable] = None       # optional condition; return True to allow
    on_enter: Optional[Callable] = None    # side effect when entering to_state


class AgentStateMachine:
    """
    State machine for agent call lifecycle.

    Valid transitions (fill these in):
    OFFLINE     + LOGIN         → ONLINE
    ONLINE      + READY         → AVAILABLE
    ONLINE      + LOGOUT        → OFFLINE
    AVAILABLE   + CALL_RECEIVED → RINGING
    AVAILABLE   + TAKE_BREAK    → BREAK
    AVAILABLE   + LOGOUT        → OFFLINE
    RINGING     + CALL_ACCEPTED → ON_CALL
    RINGING     + CALL_REJECTED → AVAILABLE
    ON_CALL     + CALL_ENDED    → WRAPPING_UP
    WRAPPING_UP + WRAP_UP_DONE  → AVAILABLE
    BREAK       + END_BREAK     → AVAILABLE
    BREAK       + LOGOUT        → OFFLINE
    """

    # TODO: Define all transitions here
    TRANSITIONS: list[StateTransition] = [
        # Example — uncomment and complete:
        # StateTransition(AgentState.OFFLINE, AgentEvent.LOGIN, AgentState.ONLINE),
    ]

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.state = AgentState.OFFLINE
        self.history: list[dict] = []
        self._state_entered_at = datetime.now()

    def trigger(self, event: AgentEvent, **metadata) -> AgentState:
        """
        Apply an event to the current state.

        Returns:
            The new AgentState after the transition.

        Raises:
            InvalidTransitionError: if the event is not valid in the current state.
        """
        # TODO: Find matching transition for (self.state, event)
        # TODO: If no match → raise InvalidTransitionError
        # TODO: If guard is set and returns False → raise InvalidTransitionError
        # TODO: Record transition in self.history
        # TODO: Call on_enter if set
        # TODO: Update self.state
        raise NotImplementedError("trigger() not implemented")

    def can_trigger(self, event: AgentEvent) -> bool:
        """
        Return True if the event is valid in the current state.
        Does NOT check guards.
        """
        # TODO: Implement this (do not raise, just return bool)
        raise NotImplementedError("can_trigger() not implemented")

    def _record_transition(self, event: AgentEvent, from_state: AgentState,
                            to_state: AgentState, **metadata):
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'agent_id': self.agent_id,
            'from_state': from_state.name,
            'event': event.name,
            'to_state': to_state.name,
            'metadata': metadata,
        })

    def get_history(self) -> list[dict]:
        return self.history
