#!/usr/bin/env python3
import unittest
from unittest.mock import PropertyMock, patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    # @parameterized.expand([("google",), ("abc",)])
    @parameterized.expand([("google",)])
    @patch('client.get_json')
    def test_org(self, org_name, mock_json):
        print("testing for org", org_name)
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
            print("RETURN:", mock_org.return_value["repos_url"])
            self.assertEqual(a._public_repos_url,
                             expected_response["repos_url"])
            self.assertEqual(b._public_repos_url,
                             expected_response["repos_url"])
