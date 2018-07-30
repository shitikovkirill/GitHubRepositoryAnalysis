import re
import urllib.request
import urllib.parse
import json


class NotValidRepositoryUrl(Exception):
    """
    Validation of repository url
    """

    def __init__(self, url):
        self.message = 'This github repository url not valid "{}"'.format(url)
        super.__init__()

    def __str__(self):
        return repr(self.message)


class RepositoryUrl:
    """
    GitHub Repository url
    """
    _url = None
    _owner = None
    _repository = None
    _url_parser_regexp = r'^(https?://)?github\.com/(?P<owner>[^/]+)/(?P<repository>[^/]+)/?$'

    def __init__(self, url):
        self._url = url
        result = re.match(self._url_parser_regexp, self._url)
        if result is None:
            raise NotValidRepositoryUrl(self._url)

        self._owner = result.group('owner')
        self._repository = result.group('repository')

    def get_owner(self):
        return self._owner

    def get_repository(self):
        return self._repository


class Repository:

    _github_api = "https://api.github.com"

    _repository_url = None
    _start = None
    _end = None
    _branch = None

    def __init__(self, url, branch='master', start=None, end=None):
        self._repository_url = RepositoryUrl(url)
        self._start = start
        self._end = end
        self._branch = branch

    def get_repository_url(self):
        return '{host}/repos/{owner}/{repo}'.format(
            host=self._github_api,
            owner=self._repository_url.get_owner(),
            repo=self._repository_url.get_repository()
        )

    def get_commits_url(self):
        return '{repository}/commits'.format(
            repository=self.get_repository_url(),
        )

    def get_commits(self, page=1):
        commits_url = self.get_commits_url()
        data = {
            'sha': self._branch,
            'page': page
        }
        if self._start:
            data['since'] = self._start

        if self._end:
            data['until'] = self._end

        return self.get_request(commits_url, parameters=data)

    @staticmethod
    def get_request(url, parameters=None):

        query_string = urllib.parse.urlencode(parameters)
        if query_string:
            url += "?" + query_string

        request = urllib.request.Request(
            url,
            headers={'Accept': 'application/vnd.github.mercy-preview+json'},
        )
        open_request = urllib.request.urlopen(request)
        data = open_request.read().decode('utf-8')
        return json.loads(data)

