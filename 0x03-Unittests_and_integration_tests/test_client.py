#!/usr/bin/env python3
import unittest
from unittest.mock import PropertyMock, patch
from parameterized import parameterized

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    # @parameterized.expand([("google",), ("abc",)])
    @parameterized.expand([("google",)])
    @patch('client.get_json')
    def test_org(self, org_name, mock_json):
        expected_response = {
            "name": org_name, "repos_url": f"https://api.github.com/orgs/{org_name}/repos"}
        mock_json.return_value = expected_response
        c = GithubOrgClient(org_name)
        c.org
        self.assertEqual(c.org, expected_response)
        mock_json.assert_called_once()
        mock_json.assert_called_once_with(c.ORG_URL.format(org=org_name))

    def test_public_repos_url(self):

        expected_response = {
            "name": "abc", "repos_url": f"https://api.github.com/orgs/abc/repos"}
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:

            mock_org.return_value = expected_response
            a = GithubOrgClient('a')
            b = GithubOrgClient('b')
            self.assertEqual(a._public_repos_url,
                             expected_response["repos_url"])
            self.assertEqual(b._public_repos_url,
                             expected_response["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_json):
        example_repo_url = "https://api.github.com/orgs/google/repos"
        test_payload = TEST_PAYLOAD[0][1]
        mock_json.return_value = test_payload
        expected_repos = []
        for repo in test_payload:
            expected_repos.append(repo['name'])

        with patch.object(GithubOrgClient, '_public_repos_url', new_callable=PropertyMock) as mock_repos_url:

            mock_repos_url.return_value = example_repo_url

            c = GithubOrgClient('google')

            self.assertEqual(c.public_repos(), expected_repos)
            self.assertEqual(c.public_repos(), expected_repos)

            # Test that the mocked property and the mocked get_json was called once.
            mock_json.assert_called_once()
            mock_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, key, expected_bool):
        self.assertEqual(GithubOrgClient.has_license(repo, key), expected_bool)
