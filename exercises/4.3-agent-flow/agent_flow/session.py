"""
agent_flow/session.py — Starter for Exercise 4.3

TODO: Implement AgentSession.process_event() and get_metrics()
"""
from datetime import datetime
from .state_machine import AgentStateMachine, AgentState, AgentEvent


class AgentSession:
    """Wraps AgentStateMachine and tracks timing/performance metrics."""

    def __init__(self, agent_id: str):
        self.machine = AgentStateMachine(agent_id)
        self.session_start = datetime.now()
        self._calls_handled = 0
        self._total_call_time_secs = 0.0
        self._total_wrap_time_secs = 0.0
        self._available_time_secs = 0.0
        self._last_state_change = self.session_start

    def process_event(self, event: AgentEvent, **kwargs) -> dict:
        """
        Process an event through the state machine.
        Track timing for calls, wrap-up, and availability.

        Returns:
            dict with keys: success (bool), new_state (str), error (str|None)
        """
        # TODO: Implement this
        # - Call self.machine.trigger(event, **kwargs)
        # - Track time spent in each state
        # - Increment _calls_handled when CALL_ENDED
        # - Handle InvalidTransitionError gracefully (return success=False)
        raise NotImplementedError("process_event() not implemented")

    def get_metrics(self) -> dict:
        """
        Return session performance metrics.

        Returns:
            {
                'agent_id': str,
                'current_state': str,
                'session_duration_secs': float,
                'calls_handled': int,
                'avg_call_duration_secs': float,
                'total_wrap_time_secs': float,
                'availability_pct': float,  # time AVAILABLE / total online time
            }
        """
        # TODO: Implement this
        raise NotImplementedError("get_metrics() not implemented")
