#!/usr/bin/env python3
"""
Test suite for client.GithubOrgClient:
- org method
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient.org method."""

    @parameterized.expand(
        [
            ("google",),
            ("abc",),
        ]
    )
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Ensure org() calls get_json and returns its payload."""
        # Arrange: set mock return value
        mock_get_json.return_value = {"login": org_name}

        # Act: create client and call org()
        client = GithubOrgClient(org_name)
        result = client.org()

        # Assert: get_json called once with correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        # Assert: result matches mocked payload
        self.assertEqual(result, {"login": org_name})
