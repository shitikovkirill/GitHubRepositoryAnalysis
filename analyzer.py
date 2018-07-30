from github_api.repository import *


class GitHubAnalyzer:

    _repository = None

    def __init__(self, url, start, end, branch):
        self._repository = Repository(url, start=start, end=end, branch=branch)

    def get_active_contributors(self):
        commits = self._repository.get_commits()
        print(commits)
        exit(1)
        return commits

