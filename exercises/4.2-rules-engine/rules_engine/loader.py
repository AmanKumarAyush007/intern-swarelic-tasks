"""
rules_engine/loader.py — Starter for Exercise 4.2

TODO: Implement load_rules_from_json() and load_rules_from_dict()
"""
import json
from pathlib import Path
from .engine import Rule, Condition, Action, VALID_ACTION_TYPES


def load_rules_from_json(path: str | Path) -> list[Rule]:
    """
    Load rules from a JSON file.

    Validates:
    - Each rule has: id, name, priority, conditions, action
    - Each condition has: field, operator, value
    - action.type is one of VALID_ACTION_TYPES
    - priority is a positive integer

    Raises:
        FileNotFoundError: if path doesn't exist
        ValueError: if any rule is malformed
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Rules file not found: {path}")

    with path.open('r', encoding='utf-8') as f:
        data = json.load(f)

    return load_rules_from_dict(data)


def load_rules_from_dict(data: list[dict]) -> list[Rule]:
    """
    Parse a list of rule dicts into Rule objects.
    Raises ValueError with helpful message if any rule is malformed.
    """
    if not isinstance(data, list):
        raise ValueError("Rules data must be a JSON array")

    rules = []
    for i, raw in enumerate(data):
        # TODO: validate and parse each rule
        # Required keys: id, name, priority, conditions, action
        # Raise ValueError(f"Rule {i}: missing key '{key}'") on missing fields
        raise NotImplementedError("load_rules_from_dict() not implemented")

    return rules
