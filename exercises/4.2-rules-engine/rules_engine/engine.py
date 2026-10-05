"""
rules_engine/engine.py — Starter for Exercise 4.2

TODO: Implement Condition.evaluate(), Rule.matches(), 
      RulesEngine.evaluate(), and RulesEngine.evaluate_all()

See docs/02-rules-engine.md for full requirements.
"""
from dataclasses import dataclass, field
from typing import Any


VALID_OPERATORS = frozenset([
    'eq', 'ne', 'gt', 'gte', 'lt', 'lte',
    'in', 'not_in', 'contains', 'startswith'
])

VALID_ACTION_TYPES = frozenset([
    'route', 'voicemail', 'escalate', 'hangup', 'play_message'
])


@dataclass
class Condition:
    field: str
    operator: str
    value: Any

    def evaluate(self, context: dict) -> bool:
        """
        Evaluate this condition against the given context dict.

        Returns False if the field is not in context.
        Raises ValueError for unknown operators.

        Supported operators:
            eq, ne, gt, gte, lt, lte,
            in, not_in, contains, startswith
        """
        if self.operator not in VALID_OPERATORS:
            raise ValueError(
                f"Unknown operator '{self.operator}'. "
                f"Valid operators: {sorted(VALID_OPERATORS)}"
            )

        if self.field not in context:
            return False

        # YOUR CODE HERE
        raise NotImplementedError("Condition.evaluate() not implemented")


@dataclass
class Action:
    type: str
    data: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.type not in VALID_ACTION_TYPES:
            raise ValueError(
                f"Invalid action type '{self.type}'. "
                f"Valid types: {sorted(VALID_ACTION_TYPES)}"
            )


@dataclass
class Rule:
    id: str
    name: str
    priority: int
    conditions: list[Condition]
    action: Action

    def matches(self, context: dict) -> bool:
        """
        Return True if ALL conditions evaluate to True.
        An empty conditions list always returns True (matches everything).
        """
        # YOUR CODE HERE
        raise NotImplementedError("Rule.matches() not implemented")


class RulesEngine:
    def __init__(self, rules: list[Rule]):
        # Rules sorted by priority (ascending — lower number = higher priority)
        self.rules = sorted(rules, key=lambda r: r.priority)

    def evaluate(self, context: dict) -> 'Action | None':
        """
        Evaluate rules in priority order.
        Return the action of the FIRST matching rule.
        Return None if no rule matches.
        """
        # YOUR CODE HERE
        raise NotImplementedError("RulesEngine.evaluate() not implemented")

    def evaluate_all(self, context: dict) -> 'list[tuple[Rule, Action]]':
        """
        Return all matching rules as (Rule, Action) tuples.
        Used for debugging and audit mode.
        """
        # YOUR CODE HERE
        raise NotImplementedError("RulesEngine.evaluate_all() not implemented")
