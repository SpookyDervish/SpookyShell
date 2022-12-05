from command import BaseCommand
from main import list_connections


class Command(BaseCommand):
    """List all available clients.

    Will display client information in a table.
    Gives information in this order:
    
    - Id
    - Ip
    - Port

    If an ip is saved, it will still appear in the list with a piece of text
    to tell the user if it is connected or not.

    Pinned ips will always appear at the top of the list.

    Examples:
        • list
    """
    HELP = "List all available clients."

    MIN_ARGS = 0
    MAX_ARGS = 1

    ARGUMENTS = {}

    def run(self, cmd_args, *args):
        list_connections(args[1], args[2])