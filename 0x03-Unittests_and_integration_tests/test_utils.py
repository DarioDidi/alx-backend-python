#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from requests import get, request
import requests
from unittest.mock import patch

from utils import access_nested_map, get_json, memoize
from client import GithubOrgClient


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError) as err:
            access_nested_map(nested_map, path)
        # self.assertEqual(err.msg, "license_key cannot be None")


class TestGetJson(unittest.TestCase):
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        # mocked request.get should have a response.json function that returns payload
        mock_get.return_value.json = lambda: test_payload
        result = get_json(test_url)
        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            test_instance = TestClass()
            res = test_instance.a_property
            print("RES:", res)
            self.assertEqual(test_instance.a_property, 42)
            self.assertEqual(test_instance.a_property, 42)
            mock_method.assert_called_once()


class TestGithubOrgClient(unittest.TestCase):
    # @parameterized.expand([("google",), ("abc",)])
    @parameterized.expand([("google",)])
    @patch('client.get_json')
    def test_org(self, org, mock_json):
        print("testing for org", org)
        mock_json.return_value = org
        c = GithubOrgClient(org)
        c.org
        self.assertEqual(c.org, org)
        mock_json.assert_called_once()
        mock_json.assert_called_once_with(c.ORG_URL.format(org=org))
