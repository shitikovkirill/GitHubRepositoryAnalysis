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
        self.print_contributors_table(contributors)

    def do_count_of_pull_requests(self, args):
        """

        :param args:
        :return:
        """
        pull_requests = self._analyzer.get_count_of_pull_requests()
        self.print_contributors_table(pull_requests)

    def default(self, line):
        print("This command does not exist")

    @staticmethod
    def print_contributors_table(data):
        print('| {:^20} | {:^10} |'.format('login', 'count commit'))
        print('-------------------------------------')
        for item in data:
            print('-------------------------------------')
            print('| {:^20} | {:^10} |'.format(str(item[0]), item[1]))


if __name__ == "__main__":
    cli = CommandLine()
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        print("Stopping session...")
