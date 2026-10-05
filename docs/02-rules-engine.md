# Exercise 4.2 — Rules Engine Implementation

## 🎯 Objective

Implement a **standalone, testable Rules Engine** inspired by the one in the Swarelic platform. This exercise teaches you:
- How to design a data-driven evaluation system
- How to write clean, extensible Python
- How production decision logic is separated from business logic

**Time estimate:** 5–6 hours

---

## Background

The Swarelic Rules Engine decides what to do with a call based on its attributes:
- Who is calling?
- What time is it?
- How many times has this number called before?
- What did the caller say?

Rules are evaluated in priority order. The **first matching rule wins** and its action is executed.

---

## 📋 What You'll Build

A pure Python rules engine (no Django needed for this exercise) with:
- A `Rule` dataclass with conditions and actions
- A `Condition` evaluator supporting multiple operators
- A `RulesEngine` class that evaluates a context against a list of rules
- A `RuleLoader` that loads rules from JSON
- Full unit tests

---

## Data Model

### Rule JSON Format

```json
[
  {
    "id": "rule-001",
    "name": "VIP Customer Bypass",
    "priority": 1,
    "conditions": [
      {"field": "caller_tag", "operator": "in", "value": ["VIP", "PREMIUM"]}
    ],
    "action": {
      "type": "route",
      "target": "vip-queue",
      "message": "Connecting you to your dedicated agent."
    }
  },
  {
    "id": "rule-002",
    "name": "After Hours",
    "priority": 2,
    "conditions": [
      {"field": "hour_of_day", "operator": "gte", "value": 21},
      {"field": "hour_of_day", "operator": "lte", "value": 8}
    ],
    "action": {
      "type": "voicemail",
      "message": "We are closed. Please leave a message."
    }
  },
  {
    "id": "rule-003",
    "name": "Repeat Caller",
    "priority": 3,
    "conditions": [
      {"field": "call_count", "operator": "gt", "value": 3}
    ],
    "action": {
      "type": "escalate",
      "target": "supervisor",
      "message": "Connecting you to a supervisor for faster resolution."
    }
  }
]
```

### Call Context

```python
context = {
    "caller_number": "+91-9876543210",
    "caller_tag": "VIP",          # VIP, PREMIUM, STANDARD, BLOCKED
    "hour_of_day": 14,            # 0–23
    "call_count": 1,              # Times this number has called
    "intent": "billing_query",    # Detected from STT
    "language": "en",
}
```

---

## 📋 Requirements

### 1. Core Classes (`rules_engine/engine.py`)

```python
from dataclasses import dataclass, field
from typing import Any

@dataclass
class Condition:
    field: str
    operator: str   # eq, ne, gt, gte, lt, lte, in, not_in, contains, startswith
    value: Any

    def evaluate(self, context: dict) -> bool:
        """
        Evaluate this condition against the given context.
        
        Operators:
          eq         → context[field] == value
          ne         → context[field] != value
          gt         → context[field] > value
          gte        → context[field] >= value
          lt         → context[field] < value
          lte        → context[field] <= value
          in         → context[field] in value  (value is a list)
          not_in     → context[field] not in value
          contains   → value in context[field]  (field is a string/list)
          startswith → str(context[field]).startswith(str(value))
        
        Returns False (not raise) if context[field] doesn't exist.
        Raises ValueError for unknown operators.
        """
        # TODO: Implement this
        pass


@dataclass
class Action:
    type: str    # route, voicemail, escalate, hangup, play_message
    data: dict = field(default_factory=dict)


@dataclass
class Rule:
    id: str
    name: str
    priority: int
    conditions: list[Condition]
    action: Action

    def matches(self, context: dict) -> bool:
        """
        Return True if ALL conditions match the context.
        Return False if ANY condition fails.
        """
        # TODO: Implement this
        pass


class RulesEngine:
    def __init__(self, rules: list[Rule]):
        # Sort by priority (lower number = higher priority)
        self.rules = sorted(rules, key=lambda r: r.priority)

    def evaluate(self, context: dict) -> Action | None:
        """
        Evaluate all rules against context.
        Return the action of the FIRST matching rule.
        Return None if no rule matches.
        """
        # TODO: Implement this
        pass

    def evaluate_all(self, context: dict) -> list[tuple[Rule, Action]]:
        """
        Return ALL matching rules (not just the first).
        Useful for debugging and audit logging.
        """
        # TODO: Implement this
        pass
```

### 2. Rule Loader (`rules_engine/loader.py`)

```python
import json
from pathlib import Path
from .engine import Rule, Condition, Action

def load_rules_from_json(path: str | Path) -> list[Rule]:
    """
    Load and parse rules from a JSON file.
    Validates:
    - Each rule has id, name, priority, conditions, action
    - Each condition has field, operator, value
    - Action type is one of: route, voicemail, escalate, hangup, play_message
    Raises ValueError on invalid rule definitions.
    """
    # TODO: Implement this
    pass

def load_rules_from_dict(data: list[dict]) -> list[Rule]:
    """Load rules from a pre-parsed list of dicts."""
    # TODO: Implement this
    pass
```

### 3. Unit Tests (`rules_engine/tests/test_engine.py`)

Write **at minimum 15 test cases** covering:

```python
import pytest
from rules_engine.engine import Condition, Rule, Action, RulesEngine

class TestCondition:
    def test_eq_operator_match(self): ...
    def test_eq_operator_no_match(self): ...
    def test_gt_operator(self): ...
    def test_in_operator(self): ...
    def test_not_in_operator(self): ...
    def test_missing_field_returns_false(self): ...
    def test_unknown_operator_raises(self): ...
    def test_contains_operator_on_list(self): ...

class TestRule:
    def test_all_conditions_must_match(self): ...
    def test_any_condition_failing_returns_false(self): ...
    def test_empty_conditions_always_matches(self): ...

class TestRulesEngine:
    def test_first_matching_rule_wins(self): ...
    def test_no_matching_rule_returns_none(self): ...
    def test_rules_sorted_by_priority(self): ...
    def test_evaluate_all_returns_all_matches(self): ...
    def test_vip_bypass_scenario(self): ...  # use the VIP rule example
```

---

## ✅ Acceptance Criteria

- [ ] `Condition.evaluate()` handles all 10 operators correctly
- [ ] `Condition.evaluate()` returns `False` for missing fields (does not raise)
- [ ] `Condition.evaluate()` raises `ValueError` for unknown operators
- [ ] `Rule.matches()` returns `True` only when ALL conditions pass
- [ ] `RulesEngine.evaluate()` returns the action of the highest-priority matching rule
- [ ] `RulesEngine.evaluate()` returns `None` when nothing matches
- [ ] `load_rules_from_json()` correctly loads the sample rules file
- [ ] All 15+ unit tests pass: `pytest rules_engine/tests/ -v`
- [ ] Code is in `submissions/<username>/4.2/`

---

## 🧪 Sample Scenario Tests

```python
# Scenario 1: VIP caller at 2 PM
context = {"caller_tag": "VIP", "hour_of_day": 14, "call_count": 1}
action = engine.evaluate(context)
assert action.type == "route"
assert action.data["target"] == "vip-queue"

# Scenario 2: Standard caller after hours
context = {"caller_tag": "STANDARD", "hour_of_day": 22, "call_count": 1}
action = engine.evaluate(context)
assert action.type == "voicemail"

# Scenario 3: Repeat caller (4 calls)
context = {"caller_tag": "STANDARD", "hour_of_day": 10, "call_count": 4}
action = engine.evaluate(context)
assert action.type == "escalate"

# Scenario 4: No matching rules
context = {"caller_tag": "STANDARD", "hour_of_day": 10, "call_count": 1}
action = engine.evaluate(context)
assert action is None
```

---

## 💡 Hints

- Keep `engine.py` pure Python — no Django, no databases
- Use `pytest` and fixtures for clean test setup
- Think about edge cases: What if `value` in `in` is not a list? What if `field` is `None`?
- The `evaluate_all` method is useful for an "audit mode" that shows all matching rules

---

## 📚 References

- Python `dataclasses` module
- `pytest` documentation
- Pattern: [Rule-based systems](https://en.wikipedia.org/wiki/Rule-based_system)
