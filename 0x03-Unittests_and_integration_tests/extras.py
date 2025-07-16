import re

regex = r"^https://api.github.com/orgs/.*/repos"
pattern = re.compile(r"^https://api.github.com/orgs/.*/repos$")
lookahead_pattern = re.compile(r"^https://api.github.com/orgs/(?!.+/.+).+")


print(bool(re.match(lookahead_pattern, "https://api.github.com/orgs/")))
print(bool(re.match(lookahead_pattern, "https://api.github.com/orgs/google/")))
print(
    bool(re.match(lookahead_pattern, "https://api.github.com/orgs/google/abc"))
)


print(__import__("test_client").__doc__)
print(__import__("test_utils").__doc__)

'''ORG_PAYLOAD = TEST_PAYLOAD[0][0]
REPOS_PAYLOAD = TEST_PAYLOAD[0][1]
EXPECTED_REPOS = TEST_PAYLOAD[0][2]
APACHE2_REPOS = TEST_PAYLOAD[0][3]

@patch('client.get_json')
def test_public_repos(mock_get_json):
    """Standalone test for public_repos without license filter"""
    # Configure the mock to return our test payloads
    mock_get_json.side_effect = [
        ORG_PAYLOAD,  # First call for org data
        REPOS_PAYLOAD  # Second call for repos data
    ]
    
    # Create client and call method
    test_class = GithubOrgClient("google")
    repos = test_class.public_repos()
    
    # Verify results
    assert repos == EXPECTED_REPOS
    
    # Verify mock calls
    assert mock_get_json.call_count == 2
    mock_get_json.assert_any_call("https://api.github.com/orgs/google")
    mock_get_json.assert_any_call("https://api.github.com/orgs/google/repos")

@patch('client.get_json')
def test_public_repos_with_license(mock_get_json):
    """Standalone test for public_repos with license filter"""
    # Configure the mock to return our test payloads
    mock_get_json.side_effect = [
        ORG_PAYLOAD,  # First call for org data
        REPOS_PAYLOAD  # Second call for repos data
    ]
    
    # Create client and call method with license filter
    test_class = GithubOrgClient("google")
    repos = test_class.public_repos(license="apache-2.0")
    
    # Verify results
    assert repos == APACHE2_REPOS
    
    # Verify mock calls
    assert mock_get_json.call_count == 2
    mock_get_json.assert_any_call("https://api.github.com/orgs/google")
    mock_get_json.assert_any_call("https://api.github.com/orgs/google/repos")

if __name__ == '__main__':
    unittest.main()
    test_public_repos()
    test_public_repos_with_license()
'''
