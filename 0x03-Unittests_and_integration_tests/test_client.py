#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from parameterized import parameterized_class
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient."""

    @parameterized.expand([
        ("google", {"login": "google", "id": 1}),
        ("abc", {"login": "abc", "id": 2}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected_payload, mock_get_json):
        """Test GithubOrgClient.org returns expected data."""
        mock_get_json.return_value = expected_payload
        result = GithubOrgClient(org_name).org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """Test internal _public_repos_url property."""
        with patch.object(
            GithubOrgClient, 'org', new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/test/repos"
            }
            result = GithubOrgClient("test")._public_repos_url
            self.assertEqual(
                result,
                "https://api.github.com/orgs/test/repos"
            )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos method returns repo names."""
        payload = [{"name": "repo1"}, {"name": "repo2"}, {"name": "repo3"}]
        mock_get_json.return_value = payload

        with patch.object(
            GithubOrgClient, '_public_repos_url', new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test/repos"
            result = GithubOrgClient("test").public_repos()
            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license static method."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


class MockResponse:
    """Mock for requests.Response with a json() method."""
    def __init__(self, json_data):
        self._json_data = json_data

    def json(self):
        return self._json_data


@parameterized_class([
    {
        "org_payload": {"repos_url": "https://api.github.com/orgs/google/repos"},
        "repos_payload": [
            {"name": "episodes.dart", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
        ],
        "expected_repos": ["episodes.dart", "repo2"],
        "apache2_repos": ["episodes.dart"]
    }
]).expand()
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                return MockResponse(cls.org_payload)
            if url == cls.org_payload["repos_url"]:
                return MockResponse(cls.repos_payload)
            return None

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        result = GithubOrgClient("google").public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        result = GithubOrgClient("google").public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)
