#!/usr/bin/env python3
"""
Test suite for client.GithubOrgClient:
- org method
- _public_repos_url property
- public_repos method
"""

from unittest.mock import Mock
from parameterized import parameterized_class
from unittest.mock import patch, MagicMock, Mock
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock, MagicMock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


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
        """calls get_json with correct URL and returns its payload."""

        # Arrange: set mock return value
        mock_get_json.return_value = {"login": org_name}

        # Act: create client and call org
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert: get_json called once with correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, {"login": org_name})


class TestGithubOrgClient(unittest.TestCase):
    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct repos_url from org"""
        with patch("client.GithubOrgClient.org",
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/testorg/repos"
            }
            client = GithubOrgClient("testorg")
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/testorg/repos")


"""Unit tests for GithubOrgClient class"""


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for the GithubOrgClient class"""

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected list of repo names"""
        mock_payload = [{"name": "repo1"}, {
            "name": "repo2"}, {"name": "repo3"}]
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


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


"""Integration test for the GithubOrgClient.public_repos method."""


@parameterized_class(("org_payload",
                      "repos_payload",
                      "expected_repos",
                      "apache2_repos"),
                     TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Set up class fixtures before any tests are run."""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            """Side effect to return mock responses based on the URL."""
            mock = Mock()
            if url == GithubOrgClient.ORG_URL.format(org="google"):
                mock.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock.json.return_value = cls.repos_payload
            return mock

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher after all tests are run."""
        cls.get_patcher.stop()


"""Integration test for the GithubOrgClient.public_repos method."""


@parameterized_class(("org_payload",
                      "repos_payload",
                      "expected_repos",
                      "apache2_repos"),
                     TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Set up class fixtures before any tests are run."""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            """Side effect to return mock responses based on the URL."""
            mock = Mock()
            if url == GithubOrgClient.ORG_URL.format(org="google"):
                mock.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock.json.return_value = cls.repos_payload
            return mock

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher after all tests are run."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method without license filter."""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos method with license filter."""
        client = GithubOrgClient("google")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)
