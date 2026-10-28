"""Validate small, explicit declarations without executing extractors or reading PDFs."""
from __future__ import annotations
import json
import re
from pathlib import Path

MAX_BYTES = 1_048_576
FIELDS = {"version", "id", "relation", "allowed_changes", "required_changes", "expected_before", "expected_after"}

class ContractError(ValueError):
    """Invalid or unsupported contract declaration."""

def _reject_number(value: str):
    raise ContractError("Floating-point and non-finite values are not supported; use decimal strings.")

def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ContractError("Duplicate JSON object key.")
        result[key] = value
    return result

def load_contract(path: str | Path) -> dict:
    # Read a bounded snapshot. This is not a sandbox for adversarial files/devices.
    with Path(path).open("rb") as source:
        raw = source.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ContractError("Contract exceeds 1 MiB.")
    try:
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object,
                          parse_float=_reject_number, parse_constant=_reject_number)
    except (UnicodeError, json.JSONDecodeError, RecursionError, ValueError) as exc:
        if isinstance(exc, ContractError):
            raise
        raise ContractError("Contract must be bounded UTF-8 JSON.") from exc
    validate_contract(data)
    return data

def _json_value(value, depth=0):
    if depth > 32:
        raise ContractError("Contract nesting exceeds 32 levels.")
    if value is None or type(value) in (str, bool, int):
        return
    if isinstance(value, list):
        for item in value:
            _json_value(item, depth + 1)
        return
    if isinstance(value, dict) and all(isinstance(k, str) for k in value):
        for item in value.values():
            _json_value(item, depth + 1)
        return
    raise ContractError("Expected JSON values without floating-point numbers.")

def _paths(value):
    if not isinstance(value, list) or any(not isinstance(p, str) for p in value):
        raise ContractError("Change paths must be an array of JSON Pointer strings.")
    if len(set(value)) != len(value):
        raise ContractError("Change paths must be unique.")
    for path in value:
        if not path.startswith("/") or re.search(r"~(?![01])", path):
            raise ContractError("Use non-root RFC 6901 JSON Pointers with valid escapes.")
    return set(value)

def _escape(token):
    return str(token).replace("~", "~0").replace("/", "~1")

def changed_paths(before, after, path=""):
    """Exact structural deltas. Added/removed containers are atomic, not wildcard paths."""
    if type(before) is not type(after):
        return {path}
    if isinstance(before, dict):
        changes = set()
        for key in before.keys() | after.keys():
            child = path + "/" + _escape(key)
            if key not in before or key not in after:
                changes.add(child)
            else:
                changes |= changed_paths(before[key], after[key], child)
        return changes
    if isinstance(before, list):
        if len(before) != len(after):
            return {path}
        changes = set()
        for index, (left, right) in enumerate(zip(before, after)):
            changes |= changed_paths(left, right, path + "/" + str(index))
        return changes
    return set() if before == after else {path}

def validate_contract(data):
    """Validate declaration consistency only; this does not evaluate an extractor."""
    if not isinstance(data, dict) or set(data) != FIELDS:
        raise ContractError("Contract must contain exactly the documented version-1 fields.")
    if type(data["version"]) is not int or data["version"] != 1:
        raise ContractError("Only integer version 1 is supported.")
    if not isinstance(data["id"], str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", data["id"]):
        raise ContractError("ID must be 1-64 lowercase letters, digits, or hyphens.")
    if data["relation"] not in ("invariant", "controlled_change"):
        raise ContractError("Unsupported relation.")
    allowed, required = _paths(data["allowed_changes"]), _paths(data["required_changes"])
    if not required <= allowed:
        raise ContractError("Required changes must be allowed.")
    for name in ("expected_before", "expected_after"):
        if not isinstance(data[name], dict):
            raise ContractError("Expected outputs must be JSON objects.")
        _json_value(data[name])
    actual = changed_paths(data["expected_before"], data["expected_after"])
    if not required <= actual <= allowed:
        raise ContractError("Expected-output delta violates declared change paths.")
    if data["relation"] == "invariant" and (allowed or required or actual):
        raise ContractError("Invariant relations must declare no changes.")
    if data["relation"] == "controlled_change" and (not required or not actual):
        raise ContractError("Controlled changes require at least one required changed path.")
    return None
