#!/usr/bin/env python3
"""Test Utility functions defined in utils.py"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
import requests
from requests import get, request

from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test the map unnesting recursion"""

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(self, nested_map, path, expected):
        """Test working example"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([({}, ("a",)), ({"a": 1}, ("a", "b"))])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that it raises an expected exception on wrong key input"""
        with self.assertRaises(KeyError) as err:
            access_nested_map(nested_map, path)
        # self.assertEqual(err.msg, "license_key cannot be None")


class TestGetJson(unittest.TestCase):
    """Test the request loop that retrieves json"""

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    @patch("requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """mocked request.get should have a response.json
        function that returns payload"""
        mock_get.return_value.json = lambda: test_payload
        result = get_json(test_url)
        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Test memoization of call results"""

    def test_memoize(self):
        """Test memoization of call results"""

        class TestClass:
            """example class just for testing"""

            def a_method(self):
                """random method"""
                return 42

            @memoize
            def a_property(self):
                """call a_method and memoizes the result"""
                return self.a_method()

        with patch.object(
            TestClass, "a_method", return_value=42
        ) as mock_method:
            test_instance = TestClass()
            self.assertEqual(test_instance.a_property, 42)
            self.assertEqual(test_instance.a_property, 42)
            mock_method.assert_called_once()
