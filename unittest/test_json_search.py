import unittest

from recursive_json_search import json_search
from test_data import data, key1, key2


class json_search_test(unittest.TestCase):
    def test_search_found(self):
        """An authorized role receives a matching value from nested data."""
        self.assertEqual(
            json_search(key1, data, role="viewer"),
            ["Network Device 10.10.20.82 Is Unreachable From Controller"],
        )

    def test_search_not_found(self):
        """A key absent from the data produces an empty result list."""
        self.assertEqual(json_search(key2, data, role="viewer"), [])

    def test_is_a_list(self):
        """Matches within dictionaries contained by a list are all retained."""
        nested_data = {
            "issues": [
                {"issueSummary": "First issue"},
                {"details": {"issueSummary": "Second issue"}},
            ]
        }
        self.assertEqual(
            json_search("issueSummary", nested_data, role="operator"),
            ["First issue", "Second issue"],
        )

    def test_viewer_cannot_read_api_key(self):
        """A viewer cannot retrieve the admin-only API key."""
        self.assertEqual(json_search("apiKey", data, role="viewer"), [])

    def test_viewer_cannot_read_management_ip_address(self):
        """A viewer cannot retrieve the admin and operator management IP."""
        self.assertEqual(json_search("managementIpAddress", data, role="viewer"), [])

    def test_operator_can_read_management_ip_address(self):
        """An operator can retrieve the management IP permitted by policy."""
        self.assertEqual(
            json_search("managementIpAddress", data, role="operator"), ["10.10.20.21"]
        )

    def test_unknown_role_is_denied(self):
        """An unrecognized role cannot retrieve even an otherwise public field."""
        self.assertEqual(json_search("issueSummary", data, role="auditor"), [])
