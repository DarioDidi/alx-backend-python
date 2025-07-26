import re

regex = r"^https://api.github.com/orgs/.*/repos"
pattern = re.compile(r"^https://api.github.com/orgs/.*/repos$")
lookahead_pattern = re.compile(r"^https://api.github.com/orgs/(?!.+/.+).+")


print(bool(re.match(lookahead_pattern, "https://api.github.com/orgs/")))
print(bool(re.match(lookahead_pattern, "https://api.github.com/orgs/google/")))
print(
    bool(re.match(lookahead_pattern, "https://api.github.com/orgs/google/abc"))
)

resp_pattern = r"FULLRESYNC \w+ 0"
print(
    bool(
        re.match(
            resp_pattern,
            "FULLRESYNC 0ee1bdb0-1123-42d5-bff0-07a50fb560fc2025 0",
        )
    )
)
