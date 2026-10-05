"""
tests/test_state_machine.py — Starter tests for Exercise 4.3

TODO: Implement all test stubs. Add at least 12 total tests.
Run with: pytest tests/ -v
"""
import pytest
from agent_flow.state_machine import (
    AgentStateMachine, AgentState, AgentEvent, InvalidTransitionError
)
from agent_flow.session import AgentSession


# ─── Valid Transition Tests ────────────────────────────────────────

class TestValidTransitions:

    def test_login_from_offline(self):
        sm = AgentStateMachine("alice")
        assert sm.state == AgentState.OFFLINE
        new_state = sm.trigger(AgentEvent.LOGIN)
        assert new_state == AgentState.ONLINE

    def test_ready_from_online(self):
        sm = AgentStateMachine("alice")
        sm.trigger(AgentEvent.LOGIN)
        sm.trigger(AgentEvent.READY)
        assert sm.state == AgentState.AVAILABLE

    def test_call_received_from_available(self):
        sm = AgentStateMachine("alice")
        sm.trigger(AgentEvent.LOGIN)
        sm.trigger(AgentEvent.READY)
        sm.trigger(AgentEvent.CALL_RECEIVED)
        assert sm.state == AgentState.RINGING

    def test_call_accepted_from_ringing(self):
        sm = AgentStateMachine("alice")
        sm.trigger(AgentEvent.LOGIN)
        sm.trigger(AgentEvent.READY)
        sm.trigger(AgentEvent.CALL_RECEIVED)
        sm.trigger(AgentEvent.CALL_ACCEPTED)
        assert sm.state == AgentState.ON_CALL

    def test_call_ended_moves_to_wrapping_up(self):
        sm = AgentStateMachine("alice")
        sm.trigger(AgentEvent.LOGIN)
        sm.trigger(AgentEvent.READY)
        sm.trigger(AgentEvent.CALL_RECEIVED)
        sm.trigger(AgentEvent.CALL_ACCEPTED)
        sm.trigger(AgentEvent.CALL_ENDED)
        assert sm.state == AgentState.WRAPPING_UP

    def test_wrap_up_done_returns_to_available(self):
        sm = AgentStateMachine("alice")
        sm.trigger(AgentEvent.LOGIN)
        sm.trigger(AgentEvent.READY)
        sm.trigger(AgentEvent.CALL_RECEIVED)
        sm.trigger(AgentEvent.CALL_ACCEPTED)
        sm.trigger(AgentEvent.CALL_ENDED)
        sm.trigger(AgentEvent.WRAP_UP_DONE)
        assert sm.state == AgentState.AVAILABLE

    def test_full_happy_path(self):
        """Complete cycle: offline → online → available → ringing → on_call → wrapping → available"""
        sm = AgentStateMachine("alice")
        for event in [
            AgentEvent.LOGIN,
            AgentEvent.READY,
            AgentEvent.CALL_RECEIVED,
            AgentEvent.CALL_ACCEPTED,
            AgentEvent.CALL_ENDED,
            AgentEvent.WRAP_UP_DONE,
        ]:
            sm.trigger(event)
        assert sm.state == AgentState.AVAILABLE

    def test_call_rejected_returns_to_available(self):
        sm = AgentStateMachine("alice")
        sm.trigger(AgentEvent.LOGIN)
        sm.trigger(AgentEvent.READY)
        sm.trigger(AgentEvent.CALL_RECEIVED)
        sm.trigger(AgentEvent.CALL_REJECTED)
        assert sm.state == AgentState.AVAILABLE


# ─── Invalid Transition Tests ─────────────────────────────────────

class TestInvalidTransitions:

    def test_cannot_accept_call_from_offline(self):
        sm = AgentStateMachine("alice")
        assert sm.state == AgentState.OFFLINE
        with pytest.raises(InvalidTransitionError):
            sm.trigger(AgentEvent.CALL_ACCEPTED)

    def test_cannot_go_on_call_directly_from_available(self):
        sm = AgentStateMachine("alice")
        sm.trigger(AgentEvent.LOGIN)
        sm.trigger(AgentEvent.READY)
        with pytest.raises(InvalidTransitionError):
            sm.trigger(AgentEvent.CALL_ACCEPTED)  # must be RINGING first

    def test_state_unchanged_after_invalid_event(self):
        sm = AgentStateMachine("alice")
        assert sm.state == AgentState.OFFLINE
        try:
            sm.trigger(AgentEvent.CALL_RECEIVED)
        except InvalidTransitionError:
            pass
        assert sm.state == AgentState.OFFLINE  # State must not change


# ─── History & Metrics Tests ──────────────────────────────────────

class TestHistory:

    def test_history_recorded_on_transition(self):
        sm = AgentStateMachine("alice")
        sm.trigger(AgentEvent.LOGIN)
        assert len(sm.get_history()) == 1
        entry = sm.get_history()[0]
        assert entry['from_state'] == 'OFFLINE'
        assert entry['event'] == 'LOGIN'
        assert entry['to_state'] == 'ONLINE'

    def test_history_grows_with_each_event(self):
        sm = AgentStateMachine("alice")
        sm.trigger(AgentEvent.LOGIN)
        sm.trigger(AgentEvent.READY)
        assert len(sm.get_history()) == 2


class TestSessionMetrics:

    def test_session_metrics_returns_required_keys(self):
        session = AgentSession("alice")
        metrics = session.get_metrics()
        required_keys = [
            'agent_id', 'current_state', 'session_duration_secs',
            'calls_handled', 'avg_call_duration_secs', 'availability_pct'
        ]
        for key in required_keys:
            assert key in metrics, f"Missing key: {key}"

    def test_calls_handled_increments(self):
        session = AgentSession("alice")
        for event in [AgentEvent.LOGIN, AgentEvent.READY, AgentEvent.CALL_RECEIVED,
                      AgentEvent.CALL_ACCEPTED, AgentEvent.CALL_ENDED, AgentEvent.WRAP_UP_DONE]:
            session.process_event(event)
        assert session.get_metrics()['calls_handled'] == 1
