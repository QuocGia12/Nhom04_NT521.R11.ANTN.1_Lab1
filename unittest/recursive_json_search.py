"""Recursive, role-aware lookup helpers for JSON-compatible data."""

from policy import POLICY


def _is_authorized(key, role):
    """Return whether *role* may read *key* according to the access policy."""
    valid_roles = {allowed_role for roles in POLICY.values() for allowed_role in roles}
    if role not in valid_roles:
        return False

    allowed_roles = POLICY.get(key)
    return allowed_roles is None or role in allowed_roles


def json_search(key, input_object, role=None):
    """Return all values stored under *key* in nested dicts and lists.

    A missing, unknown, or unauthorized role receives no results. Keys not
    listed in ``POLICY`` are treated as non-sensitive for valid roles.
    """
    if not _is_authorized(key, role):
        return []

    if isinstance(input_object, dict):
        matches = []
        for current_key, value in input_object.items():
            if current_key == key:
                matches.append(value)
            matches.extend(_search_nested(key, value))
        return matches

    if isinstance(input_object, list):
        matches = []
        for item in input_object:
            matches.extend(_search_nested(key, item))
        return matches

    return []


def _search_nested(key, input_object):
    """Recursively collect matches after access has been checked once."""
    if isinstance(input_object, dict):
        matches = []
        for current_key, value in input_object.items():
            if current_key == key:
                matches.append(value)
            matches.extend(_search_nested(key, value))
        return matches

    if isinstance(input_object, list):
        matches = []
        for item in input_object:
            matches.extend(_search_nested(key, item))
        return matches

    return []
