import re

regex = r"^https://api.github.com/orgs/.*/repos"
pattern = re.compile(r"^https://api.github.com/orgs/.*/repos$")
lookahead_pattern = re.compile(r"^https://api.github.com/orgs/(?!.+/.+).+")


print(bool(re.match(lookahead_pattern, "https://api.github.com/orgs/")))
print(bool(re.match(lookahead_pattern, "https://api.github.com/orgs/google/")))
print(
    bool(re.match(lookahead_pattern, "https://api.github.com/orgs/google/abc"))
)


print(__import__("my_module").my_function.__doc__)
