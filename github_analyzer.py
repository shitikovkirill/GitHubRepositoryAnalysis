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
    __url = None
    __owner = None
    __repository = None
    __url_parser_regexp = r'^(https?://)?github\.com/(?P<owner>[^/]+)/(?P<repository>[^/]+)/?$'

    def __init__(self, url):
        self.__url = url
        result = re.match(self.__url_parser_regexp, self.__url)
        if result is None:
            raise NotValidRepositoryUrl(self.__url)

        self.__owner = result.group('owner')
        self.__repository = result.group('repository')

    def get_owner(self):
        return self.__owner

    def get_repository(self):
        return self.__repository


class Repository:
    """
    GitHub Repository
    """
    __repository_url = None
    __data = None

    def __init__(self, url):
        self.__repository_url = RepositoryUrl(url)

    def get_contributors(self):
        url = 'https://api.github.com/repos/{owner}/{repo}/contributors'.format(
            owner=self.__repository_url.get_owner(),
            repo=self.__repository_url.get_repository()
        )
        return self.__get_request(url)

    def get_repository_info(self):
        url = 'https://api.github.com/repos/{owner}/{repo}'.format(
            owner=self.__repository_url.get_owner(),
            repo=self.__repository_url.get_repository()
        )
        return self.__get_request(url)

    @staticmethod
    def __get_request(url):
        request = urllib.request.Request(
            url,
            headers={'Accept': 'application/vnd.github.mercy-preview+json'}
        )
        open_request = urllib.request.urlopen(request)
        data = open_request.read().decode('utf-8')
        return json.loads(data)


class GitHubAnalyzer(cmd.Cmd):
    """
    GitHubAnalyzer
    """
    __repository = None

    def __init__(self):
        cmd.Cmd.__init__(self)
        try:
            url = sys.argv[1]
            self.__repository = Repository(url)
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
        contributors = self.__repository.get_contributors()
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
