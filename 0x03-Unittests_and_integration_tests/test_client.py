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


from unittest.mock import patch, PropertyMock
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


"""Unit tests for GithubOrgClient class"""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for the GithubOrgClient class"""

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected list of repo names"""
        mock_payload = [{"name": "repo1"}, {"name": "repo2"}, {"name": "repo3"}]
        mock_get_json.return_value = mock_payload

        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://fake-url.com"
            client = GithubOrgClient("testorg")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with("https://fake-url.com")
            mock_url.assert_called_once()
