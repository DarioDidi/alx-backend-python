#!/usr/bin/env python3
"""
Test functionality of GithubOrgClient class
"""
import requests
import re
import unittest
from unittest.mock import PropertyMock, patch
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """TestGithubOrgClient class"""

    @parameterized.expand([("google",)])
    @patch("client.get_json")
    def test_org(self, org_name, mock_json):
        """Test that GithubOrgClient.org returns the correct value"""
        expected_response = {
            "name": org_name,
            "repos_url": f"https://api.github.com/orgs/{org_name}/repos",
        }
        mock_json.return_value = expected_response
        c = GithubOrgClient(org_name)
        c.org
        self.assertEqual(c.org, expected_response)
        mock_json.assert_called_once()
        mock_json.assert_called_once_with(c.ORG_URL.format(org=org_name))

        def __doc__():
            pass

    def test_public_repos_url(self):
        """Test that _public_repos_url
        returns the correct value from the org payload"""
        expected_response = {
            "name": "abc",
            "repos_url": f"https://api.github.com/orgs/abc/repos",
        }
        with patch.object(
            GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:

            mock_org.return_value = expected_response
            a = GithubOrgClient("a")
            b = GithubOrgClient("b")
            self.assertEqual(
                a._public_repos_url, expected_response["repos_url"]
            )
            self.assertEqual(
                b._public_repos_url, expected_response["repos_url"]
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_json):
        """Test that public_repos returns the correct list of repos"""
        example_repo_url = "https://api.github.com/orgs/google/repos"
        test_payload = TEST_PAYLOAD[0][1]
        mock_json.return_value = test_payload
        expected_repos = []
        for repo in test_payload:
            expected_repos.append(repo["name"])

        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_repos_url:

            mock_repos_url.return_value = example_repo_url

            c = GithubOrgClient("google")

            self.assertEqual(c.public_repos(), expected_repos)
            self.assertEqual(c.public_repos(), expected_repos)

            # Test that the mocked property
            # and the mocked get_json was called once.
            mock_json.assert_called_once()
            mock_repos_url.assert_called_once()

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo, key, expected_bool):
        """check if a github client has a valid license"""
        self.assertEqual(GithubOrgClient.has_license(repo, key), expected_bool)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (
            TEST_PAYLOAD[0][0],
            TEST_PAYLOAD[0][1],
            TEST_PAYLOAD[0][2],
            TEST_PAYLOAD[0][3],
        ),
    ],
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient
        with requests mocked
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Set up class with mock patcher"""
        cls.get_patcher = patch("requests.get", return_value=TEST_PAYLOAD)
        cls.mock_get = cls.get_patcher.start()
        # cls.mock_get.return_value =

        def side_effect(url):
            """return different payloads based on URL"""
            # """if pattern ends in repos"""
            pattern = re.compile(r"^https://api.github.com/orgs/.*/repos$")
            if re.match(pattern, url):
                cls.mock_get.json = lambda: cls.repos_payload
            else:
                # look ahead patter to  check that there is no repos request
                # i.e after....orgs/, there should NOT be
                # forward slash after org name
                # that is followed by more text tested in extras.py"""
                # respond with regular org name
                lookahead_pattern = re.compile(
                    r"^https://api.github.com/orgs/(?!.+/.+).+"
                )
                if re.match(lookahead_pattern, url):
                    cls.mock_get.json = lambda: cls.org_payload

            return cls.mock_get

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos without license filter"""
        test_class = GithubOrgClient("google")
        self.assertEqual(test_class.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license filter"""
        c = GithubOrgClient("google")
        self.assertEqual(
            c.public_repos(license="apache-2.0"), self.apache2_repos
        )
