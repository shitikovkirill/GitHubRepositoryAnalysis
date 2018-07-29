#!/usr/bin/env python

import cmd
import sys
import re


class NotValidRepositoryUrl(Exception):

    def __init__(self, url):
        self.message = 'This github repository url not valid "{}"'.format(url)

    def __str__(self):
        return repr(self.message)


class Repository(object):

    @staticmethod
    def validate_url(url):
        result = re.match(r'^(https?://)?github\.com/', url)
        if result is None:
            raise NotValidRepositoryUrl(url)


class GitHubAnalyzer(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        try:
            url = sys.argv[1]
            Repository.validate_url(url)
        except IndexError:
            print('Enter the first required parameter URL (url on github repository)')
            exit(1)

        self.prompt = "> "
        self.intro = "Welcome! \n For the help, dial 'help'"

    def do_hello(self, args):
        print("hello world")

    def default(self, line):
        print("This command does not exist")


if __name__ == "__main__":
    cli = GitHubAnalyzer()
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        print("Stopping session...")
