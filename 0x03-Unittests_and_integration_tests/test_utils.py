#!/usr/bin/env python3
from utils import memoize
from unittest import TestCase
from unittest.mock import patch


class TestMemoize(TestCase):

    def test_memoize(self):
        """
        Test memoize decorator.
        This test checks if the memoize decorator correctly caches the result of a method.

        Returns:
            _type_: _description_
        """

        class TestClass:

            def a_method(self):
                return 42

            # Using memoize to cache the result of a_method
            @memoize
            def a_property(self):
                return self.a_method()

            # Using memoize to cache the result of a_method

        obj = TestClass()
        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            first = obj.a_property
            second = obj.a_property
            self.assertEqual(first, 42)
            self.assertEqual(second, 42)
            mock_method.assert_called_once()
