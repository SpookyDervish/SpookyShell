from command import BaseCommand
from util import InteractiveExit

class Command(BaseCommand):
    """Exit the interactive shell.

    If any available connections are running, the user will be prompted before
    quitting.

    Quit will always print a goodbye message before exitting.
    """
    HELP: str = "Exit the interactive shell."
    MIN_ARGS = 0
    MAX_ARGS = 0

    def run(self, cmd_args, *args):
        raise InteractiveExit