import re
import urllib.request
import urllib.parse
import json


class NotValidRepositoryTime(Exception):
    """
    Validation of repository url
    """

    def __init__(self):
        self.message = 'You mast add time in this format "YYYY-MM-DDTHH:MM:SSZ"'
        super.__init__()

    def __str__(self):
        return repr(self.message)


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


class RepositoryTime:
    _time_regexp = "\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[1-2]\d|3[0-1])T(?:[0-1]\d|2[0-3]):[0-5]\d:[0-5]\dZ"

    def validate(self, time):
        if time is None:
            return
        result = re.match(self._time_regexp, time)
        if result is None:
            raise NotValidRepositoryTime


class Repository:

    _github_api = "https://api.github.com"

    _repository_url = None
    _start = None
    _end = None
    _branch = None

    def __init__(self, url, branch='master', start=None, end=None):
        self._repository_url = RepositoryUrl(url)

        time = RepositoryTime()
        time.validate(start)
        time.validate(end)
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

    def get_request(self, url, parameters=None):
        def execute_request(commit_url):
            request = urllib.request.Request(
                commit_url,
                headers={
                    'Accept': 'application/vnd.github.v3+json',
                },
            )
            return urllib.request.urlopen(request)

        def return_commit(commit_open_request):
            data = commit_open_request.read().decode('utf-8')
            return json.loads(data)

        query_string = urllib.parse.urlencode(parameters)
        if query_string:
            url += "?" + query_string

        open_request = execute_request(url)
        commits = return_commit(open_request)

        next_link = self.find_next_link(open_request.getheader('link'))

        while next_link:
            open_request = execute_request(next_link)
            commits += return_commit(open_request)
            print('.', end='')
            next_link = self.find_next_link(open_request.getheader('link'))
        print('.')
        return commits

    @staticmethod
    def find_next_link(links):
        if not links:
            return None
        for link in links.split(','):
            url, name = link.split(';')
            if name.strip() == 'rel="next"':
                return url.strip()[1:-1]
