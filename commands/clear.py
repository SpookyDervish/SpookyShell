from command import BaseCommand
from util import clear_screen


class Command(BaseCommand):
    """Clears the screen.\n

    Will use a different command based on the operating system the user is using.\n

    On Windows it uses `cls`.\n
    On Macintosh it uses `clear`.\n
    On Linux it uses `clear`.

    Examples:
        • clear
    """
    HELP = "Clears the screen."

    MIN_ARGS = 0
    MAX_ARGS = 0

    ARGUMENTS = {}

    def run(self, cmd_args, *args):
        clear_screen()