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
    """Test suite for GithubOrgClient.org method."""

    @parameterized.expand(
        [
            ("google",),
            ("abc",),
        ]
    )
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Ensure org() calls get_json with correct URL and returns its payload."""

        # Arrange: set mock return value
        mock_get_json.return_value = {"login": org_name}

        # Act: create client and call org
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert: get_json called once with correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, {"login": org_name})


from unittest.mock import patch,PropertyMock
from client import GithubOrgClient
import unittest


class TestGithubOrgClient(unittest.TestCase):
    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct repos_url from org"""
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/testorg/repos"
            }
            client = GithubOrgClient("testorg")
            self.assertEqual(
                client._public_repos_url, "https://api.github.com/orgs/testorg/repos"
            )
