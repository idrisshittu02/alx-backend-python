#!/usr/bin/env python3
"""Unit tests for client module"""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct data"""
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected URL from org"""
        with patch.object(GithubOrgClient, 'org',
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/test_org/repos"
            }

            client = GithubOrgClient("test_org")
            result = client._public_repos_url
            expected = "https://api.github.com/orgs/test_org/repos"
            self.assertEqual(result, expected)
    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list of repo names"""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_payload

        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
             mock_url.return_value = "http://mocked_url"
             client = GithubOrgClient("test_org")
             result = client.public_repos()

             self.assertEqual(result, ["repo1", "repo2", "repo3"])
             mock_url.assert_called_once()
             mock_get_json.assert_called_once_with("http://mocked_url")
