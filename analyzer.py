from github_api.repository import *
from collections import Counter
from datetime import datetime, timedelta


class GitHubAnalyzer:

    _repository = None
    _start = None
    _end = None
    _old_pull_requests_days = 30
    _old_issues_days = 14

    def __init__(self, url, start, end, branch):
        if start:
            self._start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%SZ')
        if end:
            self._end = datetime.strptime(end, '%Y-%m-%dT%H:%M:%SZ')
        self._repository = Repository(url, start=start, end=end, branch=branch)

    def get_active_contributors(self):
        commits = self._repository.get_commits()

        counter = Counter(
            map(lambda commit: commit['author']['login'] if commit.get('author') else 'Anonymous', commits)
        )
        return counter.most_common(30)

    def get_pull_requests(self):
        pull_requests = self._repository.get_pull_requests()

        pull_requests = self._filter_by_date(pull_requests)

        counter = Counter(map(lambda request: request['state'], pull_requests))
        return counter.most_common()

    def get_old_pull_requests(self):
        pull_requests = self._repository.get_pull_requests(state='open')

        pull_requests = self._filter_old(pull_requests, self._old_pull_requests_days)

        counter = Counter(map(lambda request: request['state'], pull_requests))
        return counter.most_common()

    def get_issues(self):
        issues = self._repository.get_issues()

        issues = self._filter_by_date(issues)

        counter = Counter(map(lambda request: request['state'], issues))
        return counter.most_common()

    def get_old_issues(self):
        issues = self._repository.get_issues(state='open')
        issues = self._filter_old(issues, self._old_issues_days)

        counter = Counter(map(lambda request: request['state'], issues))
        return counter.most_common()

    @staticmethod
    def _filter_old(items, count_days):
        return filter(
            lambda item: (datetime.strptime(item['created_at'], '%Y-%m-%dT%H:%M:%SZ') <
                             datetime.now() - timedelta(days=count_days)),
            items
        )

    def _filter_by_date(self, items):
        if self._start or self._end:
            return filter(
                lambda item: self._compare_by_date(datetime.strptime(item['created_at'], '%Y-%m-%dT%H:%M:%SZ')),
                items
            )
        return items

    def _compare_by_date(self, date):
        if self._start:
            return date > self._start

        if self._end:
            return date < self._end

        return True



