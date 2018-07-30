from github_api.repository import *
from collections import Counter


class GitHubAnalyzer:

    _repository = None

    def __init__(self, url, start, end, branch):
        self._repository = Repository(url, start=start, end=end, branch=branch)

    def get_active_contributors(self):
        commits = self._repository.get_commits()

        counter = Counter(map(lambda commit: commit['author']['login'] if commit.get('author') else None, commits))
        return counter.most_common(30)



