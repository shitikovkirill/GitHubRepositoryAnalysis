import cmd
import sys
from analyzer import GitHubAnalyzer


class CommandLine(cmd.Cmd):
    """
    CommandLine
    """
    _analyzer = None

    def __init__(self):
        cmd.Cmd.__init__(self)

        start = sys.argv[2] if 2 < len(sys.argv) else None
        end = sys.argv[3] if 3 < len(sys.argv) else None
        branch = sys.argv[4] if 4 < len(sys.argv) else 'master'

        try:
            url = sys.argv[1]
            self._analyzer = GitHubAnalyzer(url, start, end, branch)
        except IndexError:
            print('Enter the first required parameter URL (url on github repository)')
            exit(1)

        self.prompt = "> "
        self.intro = "Welcome! \n For the help, dial 'help'"

    def do_active_contributors(self, args):
        """
        Active participants
        :param args:
        :return:
        """
        contributors = self._analyzer.get_active_contributors()
        self.print_table(contributors, ['login', 'count commit'])

    def do_pull_requests(self, args):
        """
        Count of open and close pull requests
        :param args:
        :return:
        """
        pull_requests = self._analyzer.get_pull_requests()
        self.print_table(pull_requests, ['status', 'count'])

    def do_old_pull_requests(self, args):
        """
        Old pull requests
        :param args:
        :return:
        """
        pull_requests = self._analyzer.get_old_pull_requests()
        self.print_table(pull_requests, ['status', 'count'])

    def default(self, line):
        print("This command does not exist")

    @staticmethod
    def print_table(data, head):
        print(('| {:^20} |' * len(head)).format(*head))
        print('------------------------------------------------')
        for item in data:
            print('------------------------------------------------')
            print(('| {:^20} |' * len(item)).format(*item))


if __name__ == "__main__":
    cli = CommandLine()
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        print("Stopping session...")
