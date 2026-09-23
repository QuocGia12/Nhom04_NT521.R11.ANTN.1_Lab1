import unittest
from recursive_json_search import *
from test_data import *

class json_search_test(unittest.TestCase):
    '''test module to test search function in `recursive_json_search.py`'''

    # --- FUNCTIONAL TESTS ---
    def test_search_found(self):
        '''key should be found, return list should not be empty'''
        self.assertTrue([] != json_search(key1, data, role="admin"))

    def test_search_not_found(self):
        '''key should not be found, should return an empty list'''
        self.assertTrue([] == json_search(key2, data, role="admin"))

    def test_is_a_list(self):
        '''Should return a list'''
        self.assertIsInstance(json_search(key1, data, role="admin"), list)

    # --- SECURITY TESTS ---
    def test_viewer_cannot_read_apikey(self):
        '''viewer role has no permission to read apiKey, result must return []'''
        result = json_search("apiKey", data, role="viewer")
        self.assertEqual([], result)

    def test_admin_can_read_apikey(self):
        '''admin role has permission to read apiKey, result must not be empty'''
        result = json_search("apiKey", data, role="admin")
        self.assertNotEqual([], result)

    def test_invalid_role_rejected(self):
        '''non-existent role (hacker) accessing managementIpAddress must return []'''
        result = json_search("managementIpAddress", data, role="hacker")
        self.assertEqual([], result)

if __name__ == '__main__':
    unittest.main()