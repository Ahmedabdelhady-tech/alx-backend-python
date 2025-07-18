#!/usr/bin/env python3
from utils import get_json
from unittest import TestCase
from unittest.mock import patch, Mock
from parameterized import parameterized


class TestGetJson(TestCase):

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):

        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response
        # return function
        result = get_json(test_url)
        # sure result call get
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)
