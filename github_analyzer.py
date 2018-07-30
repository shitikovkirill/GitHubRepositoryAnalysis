#!/usr/bin/env python

"""
Analise repository on GitHub
"""

import cmd
import sys
import re
import urllib.request
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
    """
    GitHub Repository
    """
    _repository_url = None
    _data = None
    _start = None
    _end = None
    _branch = None

    def __init__(self, url, start, end, branch):
        self._repository_url = RepositoryUrl(url)
        self._start = start
        self._end = end
        self._branch = branch

    def get_commits(self):
        url = 'https://api.github.com/repos/{owner}/{repo}/commits'.format(
            owner=self._repository_url.get_owner(),
            repo=self._repository_url.get_repository()
        )
        return self.get_request(url)

    def get_contributors(self):
        url = 'https://api.github.com/repos/{owner}/{repo}/contributors'.format(
            owner=self._repository_url.get_owner(),
            repo=self._repository_url.get_repository()
        )
        return self.get_request(url)

    def get_repository_info(self):
        url = 'https://api.github.com/repos/{owner}/{repo}'.format(
            owner=self._repository_url.get_owner(),
            repo=self._repository_url.get_repository()
        )
        return self.get_request(url)

    @staticmethod
    def get_request(url, data=None):
        request = urllib.request.Request(
            url,
            headers={'Accept': 'application/vnd.github.mercy-preview+json'},
            data=data
        )
        open_request = urllib.request.urlopen(request)
        data = open_request.read().decode('utf-8')
        return json.loads(data)


class GitHubAnalyzer(cmd.Cmd):
    """
    GitHubAnalyzer
    """
    _repository = None

    def __init__(self):
        cmd.Cmd.__init__(self)

        start = sys.argv[2] if 2 < len(sys.argv) else None
        end = sys.argv[3] if 3 < len(sys.argv) else None
        branch = sys.argv[4] if 4 < len(sys.argv) else 'master'

        try:
            url = sys.argv[1]
            self._repository = Repository(url, start, end, branch)
        except IndexError:
            print('Enter the first required parameter URL (url on github repository)')
            exit(1)

        self.prompt = "> "
        self.intro = "Welcome! \n For the help, dial 'help'"

    def do_active_participants(self, args):
        """
        Active participants
        :param args:
        :return:
        """
        contributors = self._repository.get_contributors()
        sorted(contributors, key=lambda contributor: contributor['contributions'])
        print('| {:^10} | {:^10} |'.format('login', 'contributions'))
        print('-------------------------------------')
        for contributor in contributors[:30]:
            print('-------------------------------------')
            print('| {:^10} | {:^10} |'.format(contributor['login'], contributor['contributions']))

    def default(self, line):
        print("This command does not exist")


if __name__ == "__main__":
    ANALYZER = GitHubAnalyzer()
    try:
        ANALYZER.cmdloop()
    except KeyboardInterrupt:
        print("Stopping session...")
