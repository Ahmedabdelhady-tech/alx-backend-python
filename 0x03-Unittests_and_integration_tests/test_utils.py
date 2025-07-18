#!/usr/bin/env python3
"""
Test suite for utils module functions:
- access_nested_map
- get_json
- memoize decorator
"""

from utils import access_nested_map, get_json, memoize
from parameterized import parameterized
from unittest import TestCase
from unittest.mock import patch, Mock


class TestAccessNestedMap(TestCase):
    """Test access_nested_map function."""

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            (
                {"a": {"b": 2}},
                ("a",),
                {"b": 2},
            ),
            (
                {"a": {"b": 2}},
                ("a", "b"),
                2,
            ),
        ]
    )
    def test_access_nested_map(self, nested_map, path, expected):
        """Returns value for given nested_map and path."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand(
        [
            ({}, ("a",), "a"),
            ({"a": 1}, ("a", "b"), "b"),
        ]
    )
    def test_access_nested_map_exception(self, nested_map, path, key):
        """Raises KeyError when path is invalid."""
        with self.assertRaises(KeyError) as ctx:
            access_nested_map(nested_map, path)
        self.assertEqual(str(ctx.exception), f"'{key}'")


class TestGetJson(TestCase):
    """Test get_json function with mocked HTTP calls."""

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    @patch("utils.requests.get")
    def test_get_json(self, test_url, payload, mock_get):
        """Returns correct JSON payload from URL."""
        mock_response = Mock()
        mock_response.json.return_value = payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, payload)


class TestMemoize(TestCase):
    """Test memoize decorator caching behavior."""

    def test_memoize(self):
        """a_method should be called only once for multiple a_property calls."""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        obj = TestClass()
        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            first = obj.a_property
            second = obj.a_property

            self.assertEqual(first, 42)
            self.assertEqual(second, 42)
            mock_method.assert_called_once()
