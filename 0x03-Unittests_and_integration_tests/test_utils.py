#!/usr/bin/env python3
from utils import memoize
from unittest import TestCase
from unittest.mock import patch

class TestMemoize(TestCase):
    
    def test_memoize(self):
            class TestClass:

                def a_method(self):
                    return 42

                @memoize
                def a_property(self):
                    return self.a_method()
            obj = TestClass()
            with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
                first = obj.a_property
                second = obj.a_property
                self.assertEqual(first, 42)
                self.assertEqual(second, 42)
                mock_method.assert_called_once()
